from flask import Blueprint

usuariogrupodespacho_bp = Blueprint('usuariogrupodespacho', __name__)

from ..controller.usuarioGrupoDespachoController import *