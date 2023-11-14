from app.models.viaturaModel import Viatura
from ..database import db

class ComposicaoViatura(db.Model):
    __tablename__ = 'tb_composicao_viatura_cvi'
    __table_args__ = {"schema":"cad"}
    
    id = db.Column('id_composicao_viatura_cvi', db.Integer, autoincrement=True, primary_key=True)
    idViatura = db.Column('id_viatura_cvi',db.Integer, db.ForeignKey(Viatura.id), nullable=False)
    dataInicio = db.Column('dat_inicio_cvi', db.DateTime, nullable=False)
    dataFim = db.Column('dat_fim_cvi', db.DateTime, nullable=True)

    # listComposicao = db.relationship(Composicao, back_populates="composicaoViatura")
    viatura = db.relationship(Viatura)

    def __init__(self, idViatura, dataInicio):
        self.idViatura = idViatura
        self.dataInicio = dataInicio    