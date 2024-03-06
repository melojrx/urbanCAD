from app.models.composicaoViaturaModel import ComposicaoViatura
from app.models.userModel import User
from ..database import db
from ..models.ocorrenciaModel import Ocorrencia

class Despacho(db.Model):
    __tablename__ = 'tb_despacho_des'
    __table_args__ = {"schema":"cad"}
    
    id = db.Column('id_despacho_des', db.Integer, autoincrement=True, primary_key=True)
    idOcorrencia = db.Column('id_ocorrencia_des',db.Integer, db.ForeignKey(Ocorrencia.id), nullable=False)
    idComposicaoViatura= db.Column('id_composicao_viatura_des',db.Integer, db.ForeignKey(ComposicaoViatura.id), nullable=False)
    idUsuario = db.Column('id_usuario_des', db.Integer, db.ForeignKey(User.id), nullable=False)
    dataInicio = db.Column('dat_inicio_des', db.DateTime, nullable=False)
    dataFim = db.Column('dat_fim_des', db.DateTime, nullable=True)

    ocorrencia = db.relationship(Ocorrencia)
    composicaoViatura = db.relationship(ComposicaoViatura)
    user = db.relationship(User)
    despachoHistorico = db.relationship('DespachoHistorico', primaryjoin="(Despacho.id == DespachoHistorico.idDespacho) & (DespachoHistorico.dataFim == None)", back_populates='despacho', uselist=False)
    listDespachoHistorico = db.relationship('DespachoHistorico', viewonly=True)

    def __init__(self, idOcorrencia, idComposicaoViatura, idUsuario, dataInicio):
        self.idOcorrencia = idOcorrencia
        self.idComposicaoViatura = idComposicaoViatura
        self.idUsuario = idUsuario
        self.dataInicio = dataInicio