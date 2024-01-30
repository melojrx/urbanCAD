from ..database import db

class TipoOcorrencia(db.Model):
    __tablename__ = 'tb_tipo_ocorrencia_toc'
    __table_args__ = {"schema":"cad"}
    
    id = db.Column('id_tipo_ocorrencia_toc', db.Integer, autoincrement=True, primary_key=True)
    txtTipoOcorrencia = db.Column('txt_tipo_ocorrencia_toc', db.String(50), nullable=False)
    dataInicio = db.Column('dat_inicio_toc', db.DateTime, nullable=False)
    dataFim = db.Column('dat_fim_toc', db.DateTime, nullable=True)
    icon = db.Column('txt_icon_toc', db.String(10), nullable=False)

    def __init__(self, txtTipoOcorrencia, dataInicio, dataFim, icon):
        self.txtCatetxtTipoOcorrenciagoria = txtTipoOcorrencia
        self.dataInicio = dataInicio
        self.dataFim = dataFim
        self.icon = icon