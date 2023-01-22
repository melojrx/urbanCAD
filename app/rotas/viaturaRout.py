from flask import Blueprint

viatura_bp = Blueprint('viatura', __name__)

from ..controller.viaturaController import *