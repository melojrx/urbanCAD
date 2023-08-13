from ..database import db

class SubtipoOcorrencia(db.Model):
    __tablename__ = 'tb_subtipo_ocorrencia_soc'
    __table_args__ = {"schema":"cad"}
    
    id = db.Column('id_subtipo_ocorrencia_soc', db.Integer, autoincrement=True, primary_key=True)
    idTipoOcorrencia = db.Column('id_tipo_ocorrencia_soc',db.Integer, db.ForeignKey('cad.tb_categoria_cat.id_categoria_cat'), nullable=False)
    txtSubtipoOcorrencia = db.Column('txt_subtipo_ocorrencia_soc', db.String(50), nullable=False)
    dataInicio = db.Column('dat_inicio_soc', db.DateTime, nullable=False)
    dataFim = db.Column('dat_fim_soc', db.DateTime, nullable=True)

    tipoCororrencia = db.relationship("TipoCorrencia")