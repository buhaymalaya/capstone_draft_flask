from app import db
from datetime import datetime
from sqlalchemy import DateTime

class ReplyModel(db.Model):
    __tablename__ = 'replies'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text(), nullable=False)
    time_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    username = db.Column(db.String, db.ForeignKey('user.username'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)


    def save_reply(self): 
        db.session.add(self)
        db.session.commit()

    def edit_reply(self, new_body):
        self.body = new_body
        db.session.commit()

    def delete_reply(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def from_dict(cls, data):
        return cls(
            body=data['body'],
            time_created=data.get('time_created'), 
            username=data['username'],
            post_id=data['post_id']
        )
    
        