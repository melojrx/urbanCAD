from ..database import db

class Interessado(db.Model):
    __tablename__ = 'tb_interessado_int'
    __table_args__ = {"schema":"cad"}
    
    id = db.Column('id_interessado_int', db.Integer, autoincrement=True, primary_key=True)
    idOcorrencia= db.Column('id_ocorrencia_int',db.Integer, db.ForeignKey('cad.tb_ocorrencia_oco.id_ocorrencia_oco'), nullable=False)
    txtInteressado = db.Column('txt_interessado_int', db.String(100), nullable=False)
    txtCpf = db.Column('txt_cpf_int', db.String(11), nullable=False)
    txtTelefone = db.Column('txt_telefone_int', db.String(11), nullable=False)
    isNoticianteVitima = db.Column('bol_vitima_int', db.Boolean)

    ocorrencia = db.relationship("Ocorrencia", back_populates="interessado") 

    def __init__(self, ocorrencia, txtInteressado, txtCpf, txtTelefone, isNoticianteVitima):
        self.ocorrencia = ocorrencia
        self.txtInteressado = txtInteressado
        self.txtCpf = txtCpf
        self.txtTelefone = txtTelefone
        self.isNoticianteVitima = isNoticianteVitima

