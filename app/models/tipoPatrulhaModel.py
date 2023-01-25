from ..database import db

class TipoPatrulha(db.Model):
    __tablename__ = 'tb_tipo_patrulha_tpa'
    __table_args__ = {"schema":"cad"}
    
    id = db.Column('id_tipo_patrulha_tpa', db.Integer, autoincrement=True, primary_key=True)
    txtTipoPatrulha = db.Column('txt_tipo_patrulha_tpa', db.String(50), nullable=False)
    dataInicio = db.Column('dat_inicio_tpa', db.DateTime, nullable=False)
    dataFim = db.Column('dat_fim_tpa', db.DateTime, nullable=True)