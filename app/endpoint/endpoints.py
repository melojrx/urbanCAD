
from flask import jsonify
from ..rotas.endpointRout import json_bp
from sqlalchemy import text
from ..database import db
from shapely import wkt
import json

class endpoint():

    @json_bp.route('/regionaisjson')
    def regionaisjson():
        try:
            
            sql = text("SELECT id, regiao_adm, ST_AsText(geom) as geom FROM cad.tb_regionais_reg")
            listRegionais = db.engine.execute(sql)

            if(not listRegionais.rowcount):
                return jsonify({"Nenhum registro encontrado"}), 200
            
            multipolygons = []
            for row in listRegionais:

                polygon = wkt.loads(row["geom"])
                
                multipolygon_dict = {
                    "type": "Feature",
                    "geometry": polygon.__geo_interface__,
                    "properties": {
                        "idRegiao": row["id"],
                        "regiao": row["regiao_adm"]
                    }
                }

                multipolygons.append(multipolygon_dict)

            geojson_dict = {
                "type": "FeatureCollection",
                "features": multipolygons
            }
            geojson_str = json.dumps(geojson_dict)

            return geojson_str     

        except Exception as e:
            print(f"Erro: {e}")
            return jsonify({"erro": "Ocorreu um erro ao processar a solicitação"}), 500