
from app.models.userModel import User
from ..database import db

class userDao:
   
    @staticmethod
    def getListUsuario():
        return User.query.all()