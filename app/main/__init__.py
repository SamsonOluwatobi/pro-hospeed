from flask import Blueprint

main = Blueprint('main', __name__)

from app.main import routes  # This should be the only import 