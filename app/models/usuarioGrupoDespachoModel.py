from app.models.ocorrenciaModel import Ocorrencia
from app.models.grupoDespachoModel import GrupoDespacho
from app.models.userModel import User
from ..database import db


class OcorrenciaGrupoDespacho(db.Model):
    __tablename__ = 'tb_usuario_grupo_despacho_ugd'
    __table_args__ = {"schema":"cad"}
    
    id = db.Column('id_usuario_grupo_despacho_ugd', db.Integer, autoincrement=True, primary_key=True)
    idGrupoDespacho = db.Column('id_grupo_despacho_ugd', db.Integer, db.ForeignKey(GrupoDespacho.id), nullable=False)
    idUsuario = db.Column('id_usuario_ugd', db.Integer, db.ForeignKey(User.id), nullable=False)
    dataInicio = db.Column('dat_inicio_ugd', db.DateTime, nullable=False)
    dataFim = db.Column('dat_fim_ugd', db.DateTime, nullable=True)

    ocorrencia = db.relationship(Ocorrencia) 
    grupoDespacho= db.relationship(GrupoDespacho)
    usuario = db.relationship(User)

    def __init__(self, ocorrencia, idGrupoDespacho, idUsuario, dataInicio):
        self.ocorrencia = ocorrencia
        self.idGrupoDespacho = idGrupoDespacho
        self.idUsuario = idUsuario
        self.dataInicio = dataInicio