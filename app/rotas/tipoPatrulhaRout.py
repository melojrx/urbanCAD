from flask import Blueprint

tipopatrulha_bp = Blueprint('tipopatrulha', __name__)

from ..controller.tipoPatrulhaController import *