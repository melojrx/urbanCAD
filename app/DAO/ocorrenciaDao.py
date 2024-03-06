from app.models.ocorrenciaModel import Ocorrencia

from ..database import db

class OcorrenciaDao:
    
    @staticmethod
    def getOcorrenciaById(id):
        return Ocorrencia.query.filter(Ocorrencia.id == id).first()
