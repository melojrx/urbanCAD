from ..database import db
from ..models.regionaisModel import Regional

class GrupoDespacho(db.Model):
    __tablename__ = 'tb_grupo_despacho_gde'
    __table_args__ = {"schema":"cad"}
    
    id = db.Column('id_grupo_despacho_gde', db.Integer, autoincrement=True, primary_key=True)
    idRegional = db.Column('id_regional_gde',db.Integer, db.ForeignKey(Regional.id), nullable=False)
    txtNome = db.Column('txt_nome_gde', db.String(100), nullable=False)
    dataInicio = db.Column('dat_inicio_gde', db.DateTime, nullable=False)
    dataFim = db.Column('dat_fim_gde', db.DateTime, nullable=True)

    regional = db.relationship(Regional)

    def __init__(self, id, txtNome):
        self.id = id
        self.txtNome = txtNome