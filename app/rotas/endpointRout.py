from flask import Blueprint

json_bp = Blueprint('json', __name__)

from ..endpoint.endpoints import *