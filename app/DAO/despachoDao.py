
from app.models.despachoHistoricoModel import DespachoHistorico
from ..database import db

class DespachoDao:
   
    @staticmethod
    def getDespachoHistoricoModelById(id):
        return DespachoHistorico.query.filter(DespachoHistorico.id == id).first()
