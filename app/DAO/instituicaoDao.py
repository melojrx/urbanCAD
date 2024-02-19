from app.enum.rowPerPageEnum import RowPerPageEnum
from app.models.instituicaoModel import Instituicao
from ..database import db


class instituicaoDao():

    @staticmethod
    def getlistInstituicao():
        return Instituicao.query.filter(Instituicao.dataFim.is_(None)).order_by(Instituicao.txtInstituicao.desc()).all()
    
    @staticmethod
    def delete(id, dataFim):
        Instituicao.query.filter_by(id=id).update({"dataFim": dataFim})
        db.session.commit()

    @staticmethod
    def getInstituicaoById(id):
        return Instituicao.query.filter(Instituicao.id == id).first()

    @staticmethod
    def getListDezInstituicoes(page):
        return Instituicao.query.filter(Instituicao.dataFim.is_(None)).paginate(page=page, per_page=RowPerPageEnum.DEZ.value)