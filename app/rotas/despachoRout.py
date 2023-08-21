from flask import Blueprint

despacho_bp = Blueprint('despacho', __name__)

from ..controller.despachoController import *