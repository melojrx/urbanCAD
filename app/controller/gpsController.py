from flask import request
import socketio
from ..rotas.gpsRout import gps_bp
from app import logger


@gps_bp.route('/gps', methods=['POST'])
def gps():
    if request.method == 'POST':
        # print(request.get_json())
        received_data = request.get_json()
        logger.info(received_data)
        try:

            code = received_data["code"]
            lat = received_data["lat"]
            lng = received_data["lng"]

            socketio.emit('position', {'code': code, 'lat': lat, 'lng': lng})
        except KeyError as e:
            print(f"Chave ausente no JSON: {e}")
            logger.error(f"Chave ausente no JSON: {e}")
        except Exception as e:
            logger.error("NOK")
            return 'NOK'
        
        return 'OK'