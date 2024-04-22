from marshmallow import Schema, fields

class PostSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    body = fields.Str(required=True)
    time_created = fields.Str(dump_only=True)
    user_id = fields.Int(dump_only=True)

class UserSchema(Schema):
    id = fields.Str(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    first_name = fields.Str()
    last_name = fields.Str()
    zip_code = fields.Int()

class ReplySchema(Schema):
    id = fields.Str(dump_only=True)
    body = fields.Str(required=True)
    time_created = fields.Str(dump_only=True)
    user_id = fields.Int(required=True)
    post_id = fields.Int(required=True)

class EditReplySchema(Schema):
    body = fields.String(required=True)

class SearchSchema(Schema):
    keyword = fields.String(required=True)

class PostWithUserSchema(PostSchema):
    user = fields.Nested(UserSchema)

class UserWithPostSchema(UserSchema):
    post = fields.List(fields.Nested(PostSchema), dump_only=True)
    