from ..database import db

class StatusOcorrencia(db.Model):
    __tablename__ = 'tb_status_ocorrencia_sto'
    __table_args__ = {"schema":"cad"}
    
    id = db.Column('id_status_ocorrencia_sto', db.Integer, autoincrement=True, primary_key=True)
    txtStatusOcorrencia = db.Column('txt_status_ocorrencia_sto', db.String(50), nullable=False)
    dataInicio = db.Column('dat_inicio_sto', db.DateTime, nullable=False)
    dataFim = db.Column('dat_fim_sto', db.DateTime, nullable=True)

    def __init__(self, txtStatusOcorrencia, dataInicio):
        self.txtStatusOcorrencia = txtStatusOcorrencia
        self.dataInicio = dataInicio