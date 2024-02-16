from app.models.instituicaoModel import Instituicao


class instituicaoDao():

    @staticmethod
    def getlistInstituicao():
        return Instituicao.query.filter(Instituicao.dataFim.is_(None)).order_by(Instituicao.txtInstituicao.desc()).all()