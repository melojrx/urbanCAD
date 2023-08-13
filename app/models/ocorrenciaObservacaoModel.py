from app.models.ocorrenciaHistoricoModel import OcorrenciaHistorico
from app.models.userModel import User
from ..database import db


class OcorrenciaObservacao(db.Model):
    __tablename__ = 'tb_ocorrencia_observacao_eob'
    __table_args__ = {"schema":"cad"}
    
    id = db.Column('id_evento_observacao_eob', db.Integer, autoincrement=True, primary_key=True)
    idOcorrenciaHistorico = db.Column('id_ocorrencia_historico_oob',db.Integer, db.ForeignKey(OcorrenciaHistorico), nullable=False)
    idUsuario = db.Column('id_usuario_oob', db.Integer, db.ForeignKey(User.id), nullable=False)
    txtObservacao = db.Column('txt_ocorrencia_observacao_oob', db.String, nullable=False)
    dataInicio = db.Column('dat_inicio_oob', db.DateTime, nullable=False)
    dataFim = db.Column('dat_fim_oob', db.DateTime, nullable=True)

    eventoHistorico = db.relationship("OcorrenciaHistorico", back_populates="listObservacao") 
    usuario = db.relationship("User")
    
    def __init__(self, idOcorrenciaHistorico, idUsuario, txtObservacao, dataInicio):
        self.idOcorrenciaHistorico = idOcorrenciaHistorico
        self.idUsuario = idUsuario
        self.txtObservacao = txtObservacao
        self.dataInicio = dataInicio