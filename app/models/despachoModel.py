from app.models.userModel import User
from ..database import db
from ..models.ocorrenciaModel import Ocorrencia
from ..models.instituicaoModel import Instituicao

class Despacho(db.Model):
    __tablename__ = 'tb_despacho_des'
    __table_args__ = {"schema":"cad"}
    
    id = db.Column('id_despacho_des', db.Integer, autoincrement=True, primary_key=True)
    idOcorrencia= db.Column('id_ocorrencia_des',db.Integer, db.ForeignKey(Ocorrencia.id), nullable=False)
    idInstituicao= db.Column('id_instituicao_des',db.Integer, db.ForeignKey(Instituicao.id), nullable=False)
    idUsuario = db.Column('id_usuario_des', db.Integer, db.ForeignKey(User.id), nullable=False)
    dataInicio = db.Column('dat_inicio_des', db.DateTime, nullable=False)
    dataFim = db.Column('dat_fim_des', db.DateTime, nullable=True)

    ocorrencia = db.relationship(Ocorrencia)
    instituicao = db.relationship(Instituicao) 

    def __init__(self, idOcorrencia, idInstituicao, idUsuario, dataInicio):
        self.idOcorrencia = idOcorrencia
        self.idInstituicao = idInstituicao
        self.idUsuario = idUsuario
        self.dataInicio = dataInicio