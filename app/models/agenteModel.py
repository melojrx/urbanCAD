from app.models.instituicaoModel import Instituicao
from app.models.userModel import User
from ..database import db

class Agente(db.Model):
    __tablename__ = 'tb_agente_age'
    __table_args__ = {"schema":"cad"}
    
    id = db.Column('id_agente_age', db.Integer, autoincrement=True, primary_key=True)
    idInstituicao = db.Column('id_instituicao_age',db.Integer, db.ForeignKey(Instituicao.id), nullable=False)
    idUsuario = db.Column('id_usuario_age',db.Integer, db.ForeignKey(User.id), nullable=False)
    dataInicio = db.Column('dat_inicio_age', db.DateTime, nullable=False)
    dataFim = db.Column('dat_fim_age', db.DateTime, nullable=True)

    instituicao = db.relationship(Instituicao)
    usuario = db.relationship(User)

    def __init__(self, idInstituicao, idUsuario, dataInicio):
        self.idInstituicao = idInstituicao
        self.idUsuario = idUsuario
        self.dataInicio = dataInicio    