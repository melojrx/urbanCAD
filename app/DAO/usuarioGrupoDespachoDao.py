
from app.enum.rowPerPageEnum import RowPerPageEnum
from app.models.userModel import User
from app.models.usuarioGrupoDespachoModel import UsuarioGrupoDespacho
from ..database import db

class usuarioGrupoDespachoDao:
   
    @staticmethod
    def delete(id, dataFim):
        UsuarioGrupoDespacho.query.filter_by(id=id).update({"dataFim": dataFim})
        db.session.commit()

    @staticmethod
    def getUsuarioGrupoDespachoById(id):
        return UsuarioGrupoDespacho.query.filter(UsuarioGrupoDespacho.id == id).first()

    @staticmethod
    def getListDezUsuarioGrupoDespacho(page):
        return UsuarioGrupoDespacho.query.join(UsuarioGrupoDespacho.usuario).filter(UsuarioGrupoDespacho.dataFim.is_(None)).order_by(User.name.desc()).paginate(page=page, per_page=RowPerPageEnum.DEZ.value)