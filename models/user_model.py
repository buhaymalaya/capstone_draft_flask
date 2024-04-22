# create python class that will be a SQL table; same as ddl.sql think: rules of the tables

from app import db

from werkzeug.security import generate_password_hash, check_password_hash # stores/hashes user pw but will never see raw pw

class UserModel(db.Model): #sqlalchemy model class; think instructions for a lego castle 

    __tablename__ = "user" # same name as UserModel

# create attribute for each UserSchema item below
    
    id = db.Column(db.Integer, primary_key=True) #define what data type
    username = db.Column(db.String(50), nullable = False, unique = True) #string is varchar; setting constraints
    email = db.Column(db.String(50), nullable = False, unique = True)
    password_hash = db.Column(db.String, nullable = False) # we dont have access to the encryption key
    first_name = db.Column(db.String(75), nullable = False)
    last_name = db.Column(db.String(75), nullable = False)
    zip_code = db.Column(db.Integer, nullable = False)



# will also have methods (think: dml, commands)

    def save_user(self): 
        db.session.add(self)
        db.session.commit()

    def del_user(self):
        db.session.delete(self)
        db.session.commit()

    def from_dict(self, user_dict):
        # loop through dict and set to the key
        for k, v in user_dict.items():
            if k != "password": # referring to schema
            #setattr function sets key
                setattr(self, k, v)
            else:
                setattr(self, "password_hash", generate_password_hash(v))

    def check_password(self, password):
        # Check if the provided password matches the hashed password stored in the database
        return check_password_hash(self.password_hash, password)