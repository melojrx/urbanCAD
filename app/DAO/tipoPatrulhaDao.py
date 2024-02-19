from app.enum.rowPerPageEnum import RowPerPageEnum
from app.models.tipoPatrulhaModel import TipoPatrulha
from ..database import db


class tipoPatrulhaDao():

    @staticmethod
    def getlistTipoPatrulha():
        return TipoPatrulha.query.filter(TipoPatrulha.dataFim.is_(None)).order_by(TipoPatrulha.txtTipoPatrulha.desc()).all()
    
    @staticmethod
    def delete(id, dataFim):
        TipoPatrulha.query.filter_by(id=id).update({"dataFim": dataFim})
        db.session.commit()

    @staticmethod
    def getTipoPatrulhaById(id):
        return TipoPatrulha.query.filter(TipoPatrulha.id == id).first()

    @staticmethod
    def getListDezTipoPatrulha(page):
        return TipoPatrulha.query.filter(TipoPatrulha.dataFim.is_(None)).order_by(TipoPatrulha.txtTipoPatrulha.desc()).paginate(page=page, per_page=RowPerPageEnum.DEZ.value)
