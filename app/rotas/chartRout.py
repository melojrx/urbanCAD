from flask import Blueprint

chart_bp = Blueprint('chart', __name__)

from ..controller.chartController import *