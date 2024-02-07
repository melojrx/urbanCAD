from flask import Blueprint

gps_bp = Blueprint('gps', __name__)

from ..controller.gpsController import *