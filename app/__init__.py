from flask import Flask
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager 
from Config import Config
from flask_cors import CORS 
app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)
jwt = JWTManager(app)
CORS(app)
db = SQLAlchemy(app) #instantiate
migrate = Migrate(app, db) 

from schemas import SearchSchema, EditReplySchema, PostSchema, UserSchema, PostWithUserSchema, UserWithPostSchema

from models.user_model import UserModel
from models.post_model import PostModel


from resources.discussion import bp as post_bp
app.register_blueprint(post_bp)
from resources.user import bp as user_bp
app.register_blueprint(user_bp)

# embed py game into react using iframe with endpoint
from . import bnw_maze  

@app.route('/maze-game')
def maze_game():
    # Use functionality from bnw_maze.py to generate and return the maze game content
    maze_content = bnw_maze.generate_maze()
    return maze_content