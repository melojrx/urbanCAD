
from app.enum.rowPerPageEnum import RowPerPageEnum
from app.models.grupoDespachoModel import GrupoDespacho
from app.models.regionaisModel import Regional
from ..database import db

class grupoDespachoDao:
   
    @staticmethod
    def getListGrupoDespacho():
        return GrupoDespacho.query.filter(GrupoDespacho.dataFim.is_(None)).all()

    @staticmethod
    def delete(id, dataFim):
        GrupoDespacho.query.filter_by(id=id).update({"dataFim": dataFim})
        db.session.commit()

    @staticmethod
    def getGrupoDespachoById(id):
        return GrupoDespacho.query.filter(GrupoDespacho.id == id).first()

    @staticmethod
    def getListDezGrupoDespacho(page):
        return GrupoDespacho.query.join(Regional).paginate(page=page, per_page=RowPerPageEnum.DEZ.value)#.filter(GrupoDespacho.dataFim.is_(None)).order_by(Regional.txtRegiao.asc()).paginate(page=page, per_page=RowPerPageEnum.DEZ.value)