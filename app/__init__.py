from flask_login import LoginManager
from flask import Blueprint, Flask, render_template
from whitenoise import WhiteNoise


public = Blueprint('public', __name__)
@public.route('/')
def home():
        return render_template('index.html')


app = Flask(__name__)
app.wsgi_app = WhiteNoise(app.wsgi_app, root='app/static/', prefix='static/')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.debug = True
# app.config['SQLALCHEMY_ECHO'] = True

login_manager = LoginManager(app)
login_manager.login_view = "login.login"
login_manager.login_message = u"Por favor, realize o login para acessar a página"

from .rotas.loginRout import login_bp
from .rotas.despachoRout import despacho_bp
from .rotas.grupoDespachoRout import grupodespacho_bp
from .rotas.instituicaoRout import instituicao_bp
from .rotas.maletaRout import maleta_bp
from .rotas.ocorrenciaRout import ocorrencia_bp
from .rotas.tipoPatrulhaRout import tipopatrulha_bp
from .rotas.viaturaRout import viatura_bp
from .rotas.usuarioGrupoDespachoRout import usuariogrupodespacho_bp

app.register_blueprint(public)
app.register_blueprint(login_bp)
app.register_blueprint(despacho_bp)
app.register_blueprint(grupodespacho_bp)
app.register_blueprint(instituicao_bp)
app.register_blueprint(maleta_bp)
app.register_blueprint(ocorrencia_bp)
app.register_blueprint(tipopatrulha_bp)
app.register_blueprint(viatura_bp)
app.register_blueprint(usuariogrupodespacho_bp)
# print(list(app.url_map.iter_rules()), sep='\n')