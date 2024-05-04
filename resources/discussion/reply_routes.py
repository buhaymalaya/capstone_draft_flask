from flask import jsonify, request
from flask.views import MethodView
from flask_smorest import abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.reply_model import ReplyModel
from models.post_model import PostModel
from models.user_model import UserModel
from schemas import EditReplySchema, ReplySchema, PostSchema
from . import bp

# Reply to discussion board post
from flask_jwt_extended import get_jwt_identity

@bp.route('/post/<int:post_id>/reply')
class Reply(MethodView):
   
    @jwt_required()  
    @bp.arguments(ReplySchema)  
    @bp.response(201, ReplySchema)  
    def post(self, reply_data, post_id): 
        # check if the original post exists
        original_post = PostModel.query.get(post_id)
        if not original_post:
            abort(404, message="Original post not found")

        # get the current user's identity
        current_username = get_jwt_identity()

        # Retrieve the user from the database based on the username
        current_user = UserModel.query.filter_by(username=current_username).first()
        if not current_user:
            abort(404, message="User not found")

        # create a new reply instance
        reply = ReplyModel()

        # set user_id and post_id
        reply.user_id = current_user.id
        reply.post_id = post_id
        reply.body = reply_data['body']  

        reply.save_reply()

        return reply, 201



# Edit reply
# tested, only body field necessary
@bp.route('/post/reply/<int:reply_id>')  
class EditReply(MethodView):
    @jwt_required()
    @bp.arguments(EditReplySchema)
    @bp.response(200, ReplySchema)
    def put(self, reply_data, reply_id):  
        reply = ReplyModel.query.get_or_404(reply_id)
        if reply.user_id != get_jwt_identity():
            abort(403, message="You are not allowed to edit this reply.")

        reply.edit_reply(reply_data['body'])

        return reply

# Delete reply
# tested but return message is not appearing even with 204
@bp.route('/post/reply/<int:reply_id>')  

class DeleteReply(MethodView):
    @jwt_required()
    @bp.response(204)
    def delete(self, reply_id): 
        reply = ReplyModel.query.get_or_404(reply_id)
        if reply.user_id != get_jwt_identity():
            abort(403, message="You are not allowed to delete this reply.")

        reply.delete_reply()

        return {'Message': 'Reply deleted successfully'}, 204


@bp.route('/postswithreplies')
def get_posts_with_replies():
    posts = PostModel.query.all()

    replies = ReplyModel.query.all()

    # serialize posts and replies
    posts_data = PostSchema(many=True).dump(posts)
    replies_data = ReplySchema(many=True).dump(replies)

    # create nested structure containing posts and their corresponding replies
    posts_with_replies = []
    for post_data in posts_data:
        # find replies corresponding to this post
        post_replies = [reply_data for reply_data in replies_data if reply_data['post_id'] == post_data['id']]
        post_data['replies'] = post_replies
        posts_with_replies.append(post_data)

    return jsonify(posts_with_replies)