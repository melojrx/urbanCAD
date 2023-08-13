from app.models.statusOcorrenciaModel import StatusOcorrencia
from app.models.ocorrenciaModel import Ocorrencia
from app.models.ocorrenciaObservacaoModel import OcorrenciaObservacao
from app.models.statusOcorrenciaModel import StatusOcorrencia
from app.models.userModel import User
from ..database import db


class OcorrenciaHistorico(db.Model):
    __tablename__ = 'tb_ocorrencia_historico_ohi'
    __table_args__ = {"schema":"cad"}
    
    id = db.Column('id_evento_historico_ehi', db.Integer, autoincrement=True, primary_key=True)
    idOcorrencia= db.Column('id_ocorrencia_ohi',db.Integer, db.ForeignKey(Ocorrencia.id), nullable=False)
    idStatusOcorrencia = db.Column('id_status_ocorrencia_ohi', db.Integer, db.ForeignKey(StatusOcorrencia.id), nullable=False)
    idUsuario = db.Column('id_usuario_ohi', db.Integer, db.ForeignKey(User.id), nullable=False)
    dataInicio = db.Column('dat_inicio_ohi', db.DateTime, nullable=False)
    dataFim = db.Column('dat_fim_ohi', db.DateTime, nullable=True)

    ocorrencia = db.relationship(Ocorrencia) 
    statusOCorrencia= db.relationship(StatusOcorrencia)
    usuario = db.relationship(User)
    listObservacao = db.relationship(OcorrenciaObservacao, back_populates="ocorrenciaHistorico")

    def __init__(self, ocorrencia, idStatusOcorrencia, idUsuario, dataInicio):
        self.ocorrencia = ocorrencia
        self.idStatusOcorrencia = idStatusOcorrencia
        self.idUsuario = idUsuario
        self.dataInicio = dataInicio