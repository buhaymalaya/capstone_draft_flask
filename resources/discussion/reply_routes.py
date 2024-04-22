from flask import jsonify, request
from flask.views import MethodView
from flask_smorest import abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.reply_model import ReplyModel
from models.post_model import PostModel
from schemas import EditReplySchema, ReplySchema
from . import bp

# Reply to discussion board post
@bp.route('/post/<int:post_id>/reply')
class Reply(MethodView):
    # tested, but alter code further so user_id autopopulates instead of needing
    # to input in json body along with body and post_id
    # REVISIT AND REVISE
    @jwt_required()  
    @bp.arguments(ReplySchema)  
    @bp.response(201, ReplySchema)  
    def post(self, reply_data, post_id): 
        # check if the original post exists
        original_post = PostModel.query.get(post_id)
        if not original_post:
            abort(404, message="Original post not found")

        # get the current user's identity
        current_user_id = get_jwt_identity()

        # create a new reply instance
        reply = ReplyModel.from_dict(reply_data)

        # set  user_id and post_id
        reply.user_id = current_user_id
        reply.post_id = post_id

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
