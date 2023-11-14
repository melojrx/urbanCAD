from flask import Blueprint

agente_bp = Blueprint('agente', __name__)

from ..controller.agenteController import *