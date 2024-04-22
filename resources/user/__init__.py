from flask_smorest import Blueprint

bp = Blueprint('user', __name__, description= "Routes for Users")

from . import routes