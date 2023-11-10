from app.models.statusDespachoModel import StatusDespacho
from app.models.despachoModel import Despacho
from app.models.userModel import User
from ..database import db


class DespachoHistorico(db.Model):
    __tablename__ = 'tb_despacho_historico_dhi'
    __table_args__ = {"schema":"cad"}
    
    id = db.Column('id_despacho_historico_dhi', db.Integer, autoincrement=True, primary_key=True)
    idDespacho= db.Column('id_despacho_dhi',db.Integer, db.ForeignKey(Despacho.id), nullable=False)
    idStatusDespacho = db.Column('id_status_despacho_dhi', db.Integer, db.ForeignKey(StatusDespacho.id), nullable=False)
    idUsuario = db.Column('id_usuario_dhi', db.Integer, db.ForeignKey(User.id), nullable=False)
    dataInicio = db.Column('dat_inicio_dhi', db.DateTime, nullable=False)
    dataFim = db.Column('dat_fim_dhi', db.DateTime, nullable=True)

    despacho = db.relationship(Despacho, back_populates='despachoHistorico') 
    statusDespacho= db.relationship(StatusDespacho)
    usuario = db.relationship(User)

    def __init__(self, despacho, idStatusDespacho, idUsuario, dataInicio):
        self.despacho = despacho
        self.idStatusDespacho = idStatusDespacho
        self.idUsuario = idUsuario
        self.dataInicio = dataInicio