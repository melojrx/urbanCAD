from ..database import db
from geoalchemy2 import Geometry

class Regional(db.Model):
    __tablename__ = 'tb_regionais_reg'
    __table_args__ = {"schema":"cad"}
    
    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
    idInstituicao = db.Column('id_instituicao_via',db.Integer, db.ForeignKey('cad.tb_instituicao_ins.id_instituicao_ins'), nullable=False)
    geometria = db.Column(Geometry('MULTIPOLYGON'))
    txtRegiao = db.Column('regiao_adm')
    txtSecretaria = db.Column('secretaria')

    def __init__(self, idInstituicao, geometria, txtRegiao, txtSecretaria):
        self.idInstituicao = idInstituicao
        self.geometria = geometria
        self.txtRegiao = txtRegiao
        self.txtSecretaria = txtSecretaria 