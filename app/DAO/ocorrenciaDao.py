from app.models.ocorrenciaModel import Ocorrencia
from sqlalchemy import text

from ..database import db

class OcorrenciaDao:
    
    @staticmethod
    def getOcorrenciaById(id):
        return Ocorrencia.query.filter(Ocorrencia.id == id).first()
    
    @staticmethod
    def getOcorrenciaByDate():
        try:

            sql = text("select"
            " count(oco.id_ocorrencia_oco) as total, sto.txt_status_ocorrencia_sto as status"
            " from cad.tb_ocorrencia_oco oco"
            " join cad.tb_ocorrencia_historico_ohi ohi on oco.id_ocorrencia_oco = ohi.id_ocorrencia_ohi"
            " join cad.tb_status_ocorrencia_sto sto on ohi.id_status_ocorrencia_ohi = sto.id_status_ocorrencia_sto"
            " where"
            " ohi.dat_fim_ohi is null"
            " group by 2;")

            result = db.engine.execute(sql)
            row = result.fetchall()
            return row

        except Exception as e:
            raise Exception(e)

