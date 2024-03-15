from flask_login import current_user
from app.enum.statusOcorrenciaEnum import StatusOcorrenciaEnum
from app.models import statusOcorrenciaModel
from app.models.composicaoViaturaModel import ComposicaoViatura
from app.models.despachoHistoricoModel import DespachoHistorico
from app.models.despachoModel import Despacho
from app.models.grupoDespachoModel import GrupoDespacho
from app.models.interessadoModel import Interessado
from app.models.ocorrenciaGrupoDespachoModel import OcorrenciaGrupoDespacho
from app.models.ocorrenciaHistoricoModel import OcorrenciaHistorico
from app.models.ocorrenciaModel import Ocorrencia
from app.models.subtipoOcorrenciaModel import SubtipoOcorrencia
from app.models.tipoOcorrenciaModel import TipoOcorrencia
from app.models.userModel import User
from app.models.usuarioGrupoDespachoModel import UsuarioGrupoDespacho
from ..database import db
from sqlalchemy.orm import joinedload

class DespachoDao:
   
    @staticmethod
    def getDespachoHistoricoModelById(id):
        return DespachoHistorico.query.filter(DespachoHistorico.id == id).first()
    
    @staticmethod
    def getListDespachoByAdmin():
        result = (Ocorrencia.query
            .join(Interessado)
            .join(Despacho)
            .outerjoin(SubtipoOcorrencia, 'subtipoOcorrencia')
            .outerjoin(TipoOcorrencia, SubtipoOcorrencia.tipoOcorrencia)
            .join(ComposicaoViatura)
            .join(OcorrenciaHistorico)
            .options(
                joinedload('interessado'),
                joinedload('listDespacho'),
                joinedload('subtipoOcorrencia')
            )
            .filter(
                OcorrenciaHistorico.idStatusOcorrencia == StatusOcorrenciaEnum.EM_ANDAMENTO.value, 
                OcorrenciaHistorico.dataFim.is_(None))
            )
        return result.order_by(OcorrenciaHistorico.dataInicio.desc()).all()

    @staticmethod
    def getListADespacharByAdmin():
        result = (OcorrenciaHistorico.query
            .join(Ocorrencia)
            .join(Interessado)
            .outerjoin(SubtipoOcorrencia, Ocorrencia.subtipoOcorrencia)
            .outerjoin(TipoOcorrencia, SubtipoOcorrencia.tipoOcorrencia)
            .outerjoin(Despacho, Despacho.idOcorrencia == Ocorrencia.id)
            .options(
                        joinedload('ocorrencia').joinedload('interessado'),
                        joinedload('ocorrencia.subtipoOcorrencia')
                    )
            .filter(
                OcorrenciaHistorico.dataFim.is_(None),
                Despacho.id.is_(None)
                )
            )  
        return result.order_by(OcorrenciaHistorico.dataInicio.desc()).all()

    @staticmethod
    def getListDespachoByUser():

        result = (Ocorrencia.query
            .join(Interessado)
            .join(Despacho)
            .outerjoin(SubtipoOcorrencia)
            .outerjoin(TipoOcorrencia)
            .join(ComposicaoViatura)
            .join(OcorrenciaHistorico)
            .join(OcorrenciaGrupoDespacho)
            .join(GrupoDespacho)
            .join(UsuarioGrupoDespacho)
            .join(User)
            .options(
                joinedload('interessado'),
                joinedload('listDespacho'),
                joinedload('subtipoOcorrencia')
            )
            .filter(
                OcorrenciaHistorico.idStatusOcorrencia == StatusOcorrenciaEnum.EM_ANDAMENTO.value, 
                User.id == current_user.id,
                OcorrenciaHistorico.dataFim.is_(None))
            )
        return result.order_by(OcorrenciaHistorico.dataInicio.desc()).all()

    @staticmethod
    def getListADespacharByUser():
        result = (OcorrenciaHistorico.query
                .join(Ocorrencia)
                .join(Interessado)
                .outerjoin(SubtipoOcorrencia, Ocorrencia.subtipoOcorrencia)
                .outerjoin(Despacho, Despacho.idOcorrencia == Ocorrencia.id)
                .join(OcorrenciaGrupoDespacho)
                .join(GrupoDespacho)
                .join(UsuarioGrupoDespacho)
                .options(
                            joinedload('ocorrencia').joinedload('interessado'),
                            joinedload('ocorrencia.subtipoOcorrencia')
                        )
                .filter(
                    OcorrenciaHistorico.dataFim.is_(None),
                    Despacho.id.is_(None),
                    UsuarioGrupoDespacho.idUsuario == current_user.id,
                    UsuarioGrupoDespacho.dataFim.is_(None)
                )
            )
        return result.order_by(OcorrenciaHistorico.dataInicio.desc()).all()
