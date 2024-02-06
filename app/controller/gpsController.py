from flask import request
import socketio
from ..rotas.gpsRout import gps_bp


@gps_bp.route('/gps', methods=['POST'])
def gps():
    if request.method == 'POST':
        # print(request.get_json())
        received_data = request.get_json()
        try:

            code = received_data["code"]
            lat = received_data["gps_data"]["lat"]
            lng = received_data["gps_data"]["lng"]

            socketio.emit('position', {'code': code, 'lat': lat, 'lng': lng})
        except KeyError as e:
            print(f"Chave ausente no JSON: {e}")
        except Exception as e:
            return 'NOK'
        
        return 'OK'