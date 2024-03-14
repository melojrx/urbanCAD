from flask import Blueprint

notificacoes_bp = Blueprint('notificacoes', __name__)

from ..controller.notificacoesController import *