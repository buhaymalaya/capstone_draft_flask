from flask import request, jsonify 
from flask.views import MethodView
from uuid import uuid4
from flask_smorest import abort
from flask_jwt_extended import create_access_token, unset_jwt_cookies, jwt_required
from schemas import UserSchema
from . import bp
from models.user_model import UserModel

@bp.route('/user')
class UserList(MethodView):
    # tested, nothing in json body
    @bp.response(200, UserSchema(many=True))
    def get(self):
        return UserModel.query.all() 

    # tested, create new user using fields: username,
    # email, password, first_name, last_name, zip_code
    @bp.arguments(UserSchema)
    @bp.response(201, UserSchema)
    def post(self, data):

        try:
            user = UserModel()
            user.from_dict(data)
            user.save_user()
            return user
        except:
            abort(400, message="Username or email has already been taken. Please try a different one.")



# tested, nothing in json body, remember to input user_id
# in url field
@bp.route('/user/<int:id>')
class User(MethodView):

    @bp.response(200, UserSchema)
    def get(self, id):
        user = UserModel.query.get(id)
        if user:
            return user
        else:
            abort(400, msg='Invalid entry; please try again')

    # tested, once logged in, input fields same as post
    @jwt_required()
    @bp.arguments(UserSchema)
    @bp.response(200, UserSchema)
    def put(self, data, id):
        user = UserModel.query.get(id)
        if user:
            user.from_dict(data)
            user.save_user()
            return user
        else:
            abort(400, message='Invalid entry; please try again')
     
    # tested, log in, input user_id in url field
    @jwt_required()
    def delete(self, id):
        user = UserModel.query.get(id)
        if user:
            user.del_user()
            return {'Message': 'User deleted'}, 200
        abort(400, message='Invalid entry; please try again')
        


# login and logout

# tested
@bp.route('/login', methods=['POST', 'PUT', 'DELETE'])
def login():
    login_data = request.get_json()

    username = login_data['username']
    user = UserModel.query.filter_by(username = username).first()
    if user and user.check_password(login_data['password']):
        access_token = create_access_token(identity=user.id)
        return {'access_token': access_token}, 201
    
    abort(Message="Invalid user; please try again")

# tested
@bp.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"Message": "Logout successful"})
    unset_jwt_cookies(response)
    return response
