from base64 import b64encode
from app.models.userModel import User
from ..database import db
 
class DespachoObservacao(db.Model):
    __tablename__ = 'tb_despacho_observacao_dob'
    __table_args__ = {"schema":"cad"}
    
    id = db.Column('id_despacho_observacao_dob', db.Integer, autoincrement=True, primary_key=True)
    idDespachoHistorico = db.Column('id_despacho_historico_dob',db.Integer, db.ForeignKey('cad.tb_despacho_historico_dhi.id_despacho_historico_dhi'), nullable=False)
    idUsuario = db.Column('id_usuario_dob', db.Integer, db.ForeignKey(User.id), nullable=False)
    txtObservacao = db.Column('txt_despacho_observacao_dob', db.String, nullable=False)
    file = db.Column('img_file_dob', db.LargeBinary, nullable=False)
    dataInicio = db.Column('dat_inicio_dob', db.DateTime, nullable=False)
    dataFim = db.Column('dat_fim_dob', db.DateTime, nullable=True)

    # ocorrenciaHistorico = db.relationship("OcorrenciaHistorico", back_populates="listObservacao") 
    usuario = db.relationship("User")
    
    @property
    def fileBase64(self):
        if self.file:
            return b64encode(self.file).decode()

    def __init__(self, idDespachoHistorico, idUsuario, txtObservacao, file, dataInicio):
        self.idDespachoHistorico = idDespachoHistorico
        self.idUsuario = idUsuario
        self.txtObservacao = txtObservacao
        self.file = file
        self.dataInicio = dataInicio