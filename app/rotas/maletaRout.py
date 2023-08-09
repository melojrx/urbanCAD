from flask import Blueprint

maleta_bp = Blueprint('maleta', __name__)

from ..controller.maletaController import *