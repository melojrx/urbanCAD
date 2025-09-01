from app import login_manager
from ..database import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

class User(db.Model, UserMixin):
    __tablename__ = 'tb_usuario_usu'
    __table_args__ = {"schema":"comum"}
    
    id = db.Column('id_usuario_usu', db.Integer, autoincrement=True, primary_key=True)
    name = db.Column('txt_nome_usu', db.String(200), nullable=False)
    email = db.Column('txt_email_usu', db.String(200), nullable=False, unique=True)
    cpf = db.Column('txt_cpf_usu', db.String(11), nullable=False, unique=True)
    password_hash = db.Column('txt_password_hash_usu', db.String(255), nullable=True)
    role = db.Column('txt_role_usu', db.String(50), nullable=False, default='CAD_AGENTE')

    def __init__(self, name, email, cpf, password=None, role='CAD_AGENTE'):
        self.name = name
        self.email = email
        self.cpf = cpf
        self.role = role
        if password:
            self.set_password(password)

    def set_password(self, password):
        """Gera hash da senha e armazena"""
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """Verifica se a senha fornecida confere com o hash armazenado"""
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)