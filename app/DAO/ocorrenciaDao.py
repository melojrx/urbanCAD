from operator import and_
from app.enum.rowPerPageEnum import RowPerPageEnum
from app.enum.statusOcorrenciaEnum import StatusOcorrenciaEnum
from app.models.ocorrenciaHistoricoModel import OcorrenciaHistorico
from app.models.ocorrenciaModel import Ocorrencia
from sqlalchemy import text
from ..database import db

class OcorrenciaDao:
    
    @staticmethod
    def getOcorrenciaById(id):
        return Ocorrencia.query.filter(Ocorrencia.id == id).first()
    
    @staticmethod
    def getOcorrenciaByStatus():
        try:

            sql = text("select"
            " count(oco.id_ocorrencia_oco) as data, sto.txt_status_ocorrencia_sto as label"
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
        
    @staticmethod
    def getOcorrenciaByRegiao():
        try:

            sql = text("select"
            " count(oco.id_ocorrencia_oco) as data, gde.txt_nome_gde as label"
            " from cad.tb_ocorrencia_oco oco"
            " join cad.tb_ocorrencia_grupo_despacho_ogd ogd on oco.id_ocorrencia_oco = ogd.id_ocorrencia_ogd"
            " join cad.tb_grupo_despacho_gde gde on ogd.id_grupo_despacho_ogd = gde.id_grupo_despacho_gde"
            " where"
            " oco.dat_fim_oco is null"
            " group by 2;")

            result = db.engine.execute(sql)
            row = result.fetchall()
            return row

        except Exception as e:
            raise Exception(e)

    @staticmethod
    def getCountOcorrenciaTotal():
        try:
            return Ocorrencia.query.filter(Ocorrencia.dataFim.is_(None)).count()
        except Exception as e:
            raise Exception(e)

    @staticmethod
    def getCountOcorrenciaEmAndamento():
        try:
            return Ocorrencia.query.join(OcorrenciaHistorico).filter(and_(OcorrenciaHistorico.idStatusOcorrencia==StatusOcorrenciaEnum.EM_ANDAMENTO.value ,Ocorrencia.dataFim.is_(None))).count()
        except Exception as e:
            raise Exception(e)

    @staticmethod
    def getCountOcorrenciaFinalizada():
        try:
            return Ocorrencia.query.join(OcorrenciaHistorico).filter(and_(OcorrenciaHistorico.idStatusOcorrencia==StatusOcorrenciaEnum.FINALIZADO.value ,Ocorrencia.dataFim.is_(None))).count()
        except Exception as e:
            raise Exception(e)

    @staticmethod
    def getCountOcorrenciaDespachada():
        try:
            return Ocorrencia.query.join(OcorrenciaHistorico).filter(and_(OcorrenciaHistorico.idStatusOcorrencia==StatusOcorrenciaEnum.ENVIADO_PARA_DESPACHO.value ,Ocorrencia.dataFim.is_(None))).count()
        except Exception as e:
            raise Exception(e)

    @staticmethod
    def getListOcorrenciaFinalizada(page):
        return Ocorrencia.query.join(OcorrenciaHistorico).filter(OcorrenciaHistorico.idStatusOcorrencia==StatusOcorrenciaEnum.FINALIZADO.value).paginate(page=page, per_page=RowPerPageEnum.DEZ.value)                                   

