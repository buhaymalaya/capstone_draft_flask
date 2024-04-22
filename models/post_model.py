# create python class that will be a SQL table; same as ddl.sql think: rules of the tables

from app import db
from datetime import datetime
from sqlalchemy import DateTime

class PostModel(db.Model): #sqlalchemy model class; think instructions for a lego castle 

    __tablename__ = "posts" 

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(50), nullable = False, unique = True) #string is varchar; setting constraints
    body = db.Column(db.String(), nullable = True, unique = True)
    time_created = db.Column(DateTime, default=datetime.utcnow)
    
    

# will also have methods (think: dml, commands)

    def save_post(self): 
        db.session.add(self)
        db.session.commit()

    def del_post(self):
        db.session.delete(self)
        db.session.commit()

    def from_dict(self, data):
            for field in ['title', 'body', 'user_id']:  
                if field in data:
                    setattr(self, field, data[field])