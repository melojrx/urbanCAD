from flask import Blueprint

composicao_bp = Blueprint('composicao', __name__)

from ..controller.composicaoController import *