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


# changed userid to username bc react indicates undefined
# tested, nothing in json body
# in url field
@bp.route('/user/<username>')
class User(MethodView):

    @bp.response(200, UserSchema)
    def get(self, username):
        user = UserModel.query.filter_by(username=username).first()
        if user:
            return user
        else:
            abort(400, msg='Invalid entry; please try again')

    # tested, once logged in, input fields same as userschema
    @jwt_required()
    @bp.arguments(UserSchema)
    @bp.response(200, UserSchema)
    def put(self, data, username):
        user = UserModel.query.filter_by(username=username).first()
        if user:
            data = request.json
            user.username = data.get('username', user.username)
            user.email = data.get('email', user.email)
            user.first_name = data.get('first_name', user.first_name)
            user.last_name = data.get('last_name', user.last_name)
            user.zip_code = data.get('zip_code', user.zip_code)
            user.save_user()
            return user, 204
            
        else:
            abort(404, message='User not found')
     
    # tested, log in, input user_id in url field
    # delete won't work bc of replies constraint..TBD
    @jwt_required()
    def delete(self, username):
        user = UserModel.query.filter_by(username=username).first()
        if user:
            user.del_user()
            return {'Message': username + ' deleted'}, 200
        abort(404, message='Error: User not found')
        


# login and logout

# tested
@bp.route('/login', methods=['POST', 'PUT', 'DELETE', 'GET'])
def login():
    login_data = request.get_json()

    username = login_data['username']
    user = UserModel.query.filter_by(username = username).first()
    if user and user.check_password(login_data['password']):
        access_token = create_access_token(identity=user.username)
        return {'access_token': access_token, 'username': username}, 201
    
    abort(401, Message="Invalid username or password; please try again")

# tested
@bp.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"Message": "Logout successful"})
    unset_jwt_cookies(response)
    return response
