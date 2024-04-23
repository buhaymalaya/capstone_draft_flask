from flask_smorest import Blueprint

bp = Blueprint("maze", __name__, description="Routes for Maze")

from . import routes