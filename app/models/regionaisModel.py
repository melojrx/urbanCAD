from ..database import db
from geoalchemy2 import Geometry

class Regional(db.Model):
    __tablename__ = 'tb_regionais_reg'
    __table_args__ = {"schema":"cad"}
    
    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
    geom = db.Column(Geometry('geom'))
    txtRegiao = db.Column('regiao_adm', db.String(254), nullable=False)
    txtSecretaria = db.Column('secretaria', db.String(254), nullable=False)

    def __init__(self, geom, txtRegiao, txtSecretaria):
        self.geom = geom
        self.txtRegiao = txtRegiao
        self.txtSecretaria = txtSecretaria 