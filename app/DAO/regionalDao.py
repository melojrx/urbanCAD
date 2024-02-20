from app.models.regionaisModel import Regional

class regionalDao:
   
    @staticmethod
    def getListRegionais():
        return Regional.query.order_by(Regional.txtRegiao.asc()).all()