from app.models.tipoPatrulhaModel import TipoPatrulha
from ..database import db

class Viatura(db.Model):
    __tablename__ = 'tb_viatura_via'
    __table_args__ = {"schema":"cad"}
    
    id = db.Column('id_viatura_via', db.Integer, autoincrement=True, primary_key=True)
    idInstituicao = db.Column('id_instituicao_via',db.Integer, db.ForeignKey('cad.tb_instituicao_ins.id_instituicao_ins'), nullable=False)
    idTipoPatrulha = db.Column('id_tipo_patrulha_via', db.Integer, db.ForeignKey('cad.tb_tipo_patrulha_tpa.id_tipo_patrulha_tpa'), nullable=False)
    txtCodigo = db.Column('txt_codigo_via', db.String(30), nullable=False)
    txtPlaca = db.Column('txt_placa_via', db.String(7), nullable=False)
    txtDescricao = db.Column('txt_descricao_via', db.String(100), nullable=False)
    dataInicio = db.Column('dat_inicio_via', db.DateTime, nullable=False)
    dataFim = db.Column('dat_fim_via', db.DateTime, nullable=True)

    instituicao = db.relationship("Instituicao")
    tipoPatrulha = db.relationship(TipoPatrulha)

    def __str__(self):
            return f"{self.tipoPatrulha.txtTipoPatrulha} {self.instituicao.txtInstituicao} {self.txtCodigo} {self.txtPlaca}"

    def __init__(self, idInstituicao, idTipoPatrulha, txtCodigo, txtPlaca, txtDescricao, dataInicio):
        self.idInstituicao = idInstituicao
        self.idTipoPatrulha = idTipoPatrulha
        self.txtCodigo = txtCodigo
        self.txtPlaca = txtPlaca
        self.txtDescricao = txtDescricao
        self.dataInicio = dataInicio    