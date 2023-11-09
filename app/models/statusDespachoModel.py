from ..database import db

class StatusDespacho(db.Model):
    __tablename__ = 'tb_status_despacho_sde'
    __table_args__ = {"schema":"cad"}
    
    id = db.Column('id_status_despacho_sde', db.Integer, autoincrement=True, primary_key=True)
    txtStatusDespacho = db.Column('txt_status_despacho_sde', db.String(50), nullable=False)
    dataInicio = db.Column('dat_inicio_sde', db.DateTime, nullable=False)
    dataFim = db.Column('dat_fim_sde', db.DateTime, nullable=True)

    def __init__(self, txtStatusDespacho, dataInicio):
        self.txtStatusOcorrencia = txtStatusDespacho
        self.dataInicio = dataInicio