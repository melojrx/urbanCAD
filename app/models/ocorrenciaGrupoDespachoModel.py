from app.models.statusDespachoModel import StatusDespacho
from app.models.ocorrenciaModel import Ocorrencia
from app.models.grupoDespachoModel import GrupoDespacho
from app.models.userModel import User
from ..database import db


class OcorrenciaGrupoDespacho(db.Model):
    __tablename__ = 'tb_ocorrencia_grupo_despacho_ogd'
    __table_args__ = {"schema":"cad"}
    
    id = db.Column('id_ocorrencia_grupo_despacho_ogd', db.Integer, autoincrement=True, primary_key=True)
    idOcorrencia = db.Column('id_ocorrencia_ogd',db.Integer, db.ForeignKey(Ocorrencia.id), nullable=False)
    idGrupoDespacho = db.Column('id_grupo_despacho_ogd', db.Integer, db.ForeignKey(GrupoDespacho.id), nullable=False)
    idUsuario = db.Column('id_usuario_ogd', db.Integer, db.ForeignKey(User.id), nullable=False)
    dataInicio = db.Column('dat_inicio_ogd', db.DateTime, nullable=False)
    dataFim = db.Column('dat_fim_ogd', db.DateTime, nullable=True)

    ocorrencia = db.relationship(Ocorrencia) 
    grupoDespacho= db.relationship(GrupoDespacho)
    usuario = db.relationship(User)

    def __init__(self, idOcorrencia, idGrupoDespacho, idUsuario, dataInicio):
        self.idOcorrencia = idOcorrencia
        self.idGrupoDespacho = idGrupoDespacho
        self.idUsuario = idUsuario
        self.dataInicio = dataInicio