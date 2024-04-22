from flask_smorest import Blueprint

bp = Blueprint("discussion", __name__, description="Routes for Discussions")

from . import routes, reply_routes