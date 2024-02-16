from app.models.tipoPatrulhaModel import TipoPatrulha


class tipoPatrulhaDao():

    @staticmethod
    def getlistTipoPatrulha():
        return TipoPatrulha.query.filter(TipoPatrulha.dataFim.is_(None)).order_by(TipoPatrulha.txtTipoPatrulha.desc()).all()
