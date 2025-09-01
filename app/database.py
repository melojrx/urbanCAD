from app import app
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Usar variável de ambiente ou valor padrão
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/postgres')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

# Usar SECRET_KEY do ambiente ou valor padrão
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'secret')

db = SQLAlchemy(app)
"""Extensão de migração.
Para criar migrações:
    flask db init
    flask db migrate -m "mensagem"
    flask db upgrade
"""
migrate = Migrate(app, db)

@app.errorhandler(Exception)
def internal_error(e):
    db.session.rollback()
    return render_template('erro.html', e=e)