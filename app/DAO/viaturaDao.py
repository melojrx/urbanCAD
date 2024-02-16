
from app.enum.rowPerPageEnum import RowPerPageEnum
from app.models.viaturaModel import Viatura
from ..database import db

class viaturaDao:
   
    @staticmethod
    def delete(id, dataFim):
        Viatura.query.filter_by(id=id).update({"dataFim": dataFim})
        db.session.commit()

    @staticmethod
    def getViaturaById(id):
        return Viatura.query.filter(Viatura.id == id).first()

    @staticmethod
    def getListDezViaturas(page):
        return Viatura.query.filter(Viatura.dataFim.is_(None)).order_by(Viatura.txtCodigo.desc()).paginate(page=page, per_page=RowPerPageEnum.DEZ.value)