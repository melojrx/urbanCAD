from flask import Blueprint

instituicao_bp = Blueprint('instituicao', __name__)

from ..controller.instituicaoController import *