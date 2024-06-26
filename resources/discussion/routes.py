from flask import jsonify
from flask.views import MethodView
from flask_smorest import abort
from uuid import uuid4
from . import bp
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.post_model import PostModel
from models.user_model import UserModel
from schemas import UserSchema, PostSchema, PostWithUserSchema, SearchSchema
from flask_jwt_extended import get_jwt_identity

@bp.route('/post')
class DiscussionBoardList(MethodView):
    # user can create a discussion board thread by posting when logged in
    # include title and body
    @jwt_required()
    @bp.response(201, PostSchema)
    @bp.arguments(PostSchema)
    def post(self, post_data):

        try:
            # current user's ID
            username = get_jwt_identity()
            user = UserModel.query.filter_by(username=username).first()
            if user:
                post = PostModel()
                post.from_dict(post_data)
                post.user_id = user.id
                post.save_post()
                return post
            else:
                abort(400, message="User not found.")
        
        except Exception as e:
            abort(400, message=f"Failed to post: {str(e)}")


    # All posts in discussion board
    # tested, nothing in json body
    @bp.response(200, PostSchema(many=True))
    # user can view threads created by other users
    def get(self):
        return PostModel.query.all()


# search field - keyword
# tested
@bp.route('/post/search') # search?keyword=the_keyword, nothin in json body
class SearchPosts(MethodView):

    @bp.arguments(SearchSchema, location='query')
    @bp.response(200, PostSchema(many=True))
    def get(self, search_data):
        keyword = search_data.get('keyword')
        if not keyword:
            abort(400, message="Thread not found")

        posts = PostModel.query.filter(PostModel.body.ilike(f"%{keyword}%")).all()

        return posts


# SPECIFIC POSTS

@bp.route('/post/<post_id>')
class Post(MethodView):

# retrieve specific post
# tested, remember to input post_id in url
    @jwt_required()
    @bp.response(200, PostWithUserSchema)
    def get(self, post_id):
        try: 
            return PostModel.query.get(post_id)
        except:
            abort(400, message="Post not found")


# edit specific post once logged in
# tested, incl title and body in json body with auth token for user_id
    from flask_jwt_extended import get_jwt_identity

    @jwt_required()   
    @bp.arguments(PostSchema)
    @bp.response(201, PostSchema)
    def put(self, post_data, post_id):

        # Get the current user's username from the JWT token
        current_username = get_jwt_identity()

        # Retrieve the current user from the database based on the username
        current_user = UserModel.query.filter_by(username=current_username).first()

        # Check if the current user exists
        if not current_user:
            abort(404, message="User not found")

        # Retrieve the post from the database based on the post_id
        post = PostModel.query.get(post_id)
        if not post:
            abort(400, message="Post not found")

        # Check if the current user is the owner of the post
        if current_user.id != post.user_id:
            abort(403, message="You are not allowed to edit this post.")

        # Update the post attributes and save it
        post_data['user_id'] = current_user.id
        post.from_dict(post_data)
        post.save_post()

        return post



# delete specific post once logged in
# tested
    @jwt_required()   
    def delete(self, post_id):

        post = PostModel.query.get(post_id)

        if not post:
            abort(400, message="Post not found")

        post.del_post()
        return {'Message': f"Post: {post_id} deleted"}, 200


