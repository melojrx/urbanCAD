from flask import Blueprint

grupodespacho_bp = Blueprint('grupodespacho', __name__)

from ..controller.grupoDespachoController import *