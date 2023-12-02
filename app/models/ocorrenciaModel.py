from app.models.interessadoModel import Interessado
from app.models.userModel import User
from app.models.subtipoOcorrenciaModel import SubtipoOcorrencia
from ..database import db

class Ocorrencia(db.Model):
    __tablename__ = 'tb_ocorrencia_oco'
    __table_args__ = {"schema":"cad"}
    
    id = db.Column('id_ocorrencia_oco', db.Integer, autoincrement=True, primary_key=True)
    idSubtipoOcorrenia = db.Column('id_subtipo_ocorrencia_oco',db.Integer, db.ForeignKey(SubtipoOcorrencia.id), nullable=False)
    idUsuario = db.Column('id_usuario_oco', db.Integer, db.ForeignKey(User.id), nullable=False)
    numOcorrencia = db.Column('num_ocorrencia_oco', db.String(11), nullable=False)
    txtProblema = db.Column('txt_problema_oco', db.String(1000), nullable=False)
    txtEndereco = db.Column('txt_endereco_oco', db.String(500), nullable=False)
    txtLat = db.Column('txt_latitude_oco', db.String(20), nullable=False)
    txtLong = db.Column('txt_longitude_oco', db.String(20), nullable=False)
    dataInicio = db.Column('dat_inicio_oco', db.DateTime, nullable=False)
    dataFim = db.Column('dat_fim_oco', db.DateTime, nullable=True)
    fileBase64 = None
    
    usuario = db.relationship(User)
    subcategoria = db.relationship(SubtipoOcorrencia)
    interessado = db.relationship(Interessado, back_populates="ocorrencia", uselist=False)
    ocorrenciaHistorico = db.relationship('OcorrenciaHistorico', primaryjoin="(Ocorrencia.id == OcorrenciaHistorico.idOcorrencia) & (OcorrenciaHistorico.dataFim == None)", back_populates='ocorrencia', uselist=False)
    listDespacho = db.relationship("Despacho", back_populates='ocorrencia')

    def __init__(self, idSubtipoOcorrenia, idUsuario, numOcorrencia, txtProblema, txtEndereco, txtLat, txtLong, dataInicio):
        self.idSubtipoOcorrenia = idSubtipoOcorrenia
        self.idUsuario = idUsuario
        self.numOcorrencia = numOcorrencia
        self.txtProblema = txtProblema
        self.txtEndereco = txtEndereco
        self.txtLat = txtLat
        self.txtLong = txtLong
        self.dataInicio = dataInicio