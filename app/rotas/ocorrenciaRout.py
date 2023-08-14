from flask import Blueprint

ocorrencia_bp = Blueprint('ocorrencia', __name__)

from ..controller.ocorrenciaController import *