# from app.models.agenteModel import Agente
# from app.models.composicaoViaturaModel import ComposicaoViatura
# from ..database import db

# class Composicao(db.Model):
#     __tablename__ = 'tb_composicao_com'
#     __table_args__ = {"schema":"cad"}
    
#     id = db.Column('id_composicao_com', db.Integer, autoincrement=True, primary_key=True)
#     idComposicaoViatura = db.Column('id_composicao_viatura_com',db.Integer, db.ForeignKey(ComposicaoViatura.id), nullable=False)
#     idAgente = db.Column('id_agente_com',db.Integer, db.ForeignKey(Agente.id), nullable=False)
#     dataInicio = db.Column('dat_inicio_com', db.DateTime, nullable=False)
#     dataFim = db.Column('dat_fim_com', db.DateTime, nullable=True)

#     composicaoViatura = db.relationship(ComposicaoViatura)
#     agente = db.relationship(Agente)

#     def __init__(self, composicaoViatura, idAgente, dataInicio):
#         self.composicaoViatura = composicaoViatura
#         self.idAgente = idAgente
#         self.dataInicio = dataInicio    