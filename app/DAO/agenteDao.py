
from app.enum.rowPerPageEnum import RowPerPageEnum
from app.models.agenteModel import Agente
from ..database import db

class agenteDao:
   
    @staticmethod
    def delete(id, dataFim):
        Agente.query.filter_by(id=id).update({"dataFim": dataFim})
        db.session.commit()

    @staticmethod
    def getAgenteById(id):
        return Agente.query.filter(Agente.id == id).first()

    @staticmethod
    def getListDezAgentes(page):
        return Agente.query.filter(Agente.dataFim.is_(None)).paginate(page=page, per_page=RowPerPageEnum.DEZ.value)