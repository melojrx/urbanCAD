from ..database import db

class Viatura(db.Model):
    __tablename__ = 'tb_viatura_via'
    __table_args__ = {"schema":"cad"}
    
    id = db.Column('id_viatura_via', db.Integer, autoincrement=True, primary_key=True)
    txtCodigo = db.Column('txt_codigo_via', db.String(30), nullable=False)
    txtDescricao = db.Column('txt_descricao_via', db.String(100), nullable=False)
    dataInicio = db.Column('dat_inicio_via', db.DateTime, nullable=False)
    dataFim = db.Column('dat_fim_via', db.DateTime, nullable=True)


    def __init__(self, txtCodigo, txtDescricao, dataInicio):
        self.txtCodigo = txtCodigo
        self.txtDescricao = txtDescricao
        self.dataInicio = dataInicio    