from ..database import db

class Instituicao(db.Model):
    __tablename__ = 'tb_instituicao_ins'
    __table_args__ = {"schema":"cad"}
    
    id = db.Column('id_instituicao_ins', db.Integer, autoincrement=True, primary_key=True)
    txtInstituicao = db.Column('txt_instituicao_ins', db.String(50), nullable=False)
    dataInicio = db.Column('dat_inicio_ins', db.DateTime, nullable=False)
    dataFim = db.Column('dat_fim_ins', db.DateTime, nullable=True)