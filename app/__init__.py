from flask_login import LoginManager
from flask import Flask
from whitenoise import WhiteNoise
from flask_socketio import SocketIO
from flask_cors import CORS
import logging
import secrets

app = Flask(__name__)
app.wsgi_app = WhiteNoise(app.wsgi_app, root='app/static/', prefix='static/')
# socketio = SocketIO(app, async_mode='gevent', manage_session=False)
socketio = SocketIO(app, manage_session=False, session_cookie=True)
app.config['SECRET_KEY'] = secrets.token_hex(16)
CORS(app, resources={r"/socket.io/*": {"origins": "*"}})
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# app.debug = True
#app.config['SQLALCHEMY_ECHO'] = True

login_manager = LoginManager(app)
login_manager.login_view = "login.login"
login_manager.login_message = u"Por favor, realize o login para acessar a página"

from .rotas.agenteRout import agente_bp
from .rotas.loginRout import login_bp
from .rotas.composicaoRout import composicao_bp
from .rotas.despachoRout import despacho_bp
from .rotas.gpsRout import gps_bp
from .rotas.endpointRout import json_bp
from .rotas.grupoDespachoRout import grupodespacho_bp
from .rotas.instituicaoRout import instituicao_bp
from .rotas.ocorrenciaRout import ocorrencia_bp
from .rotas.publicRout import public_bp
from .rotas.tipoPatrulhaRout import tipopatrulha_bp
from .rotas.viaturaRout import viatura_bp
from .rotas.usuarioGrupoDespachoRout import usuariogrupodespacho_bp
from .rotas.dashboardRout import dashboard_bp
from .rotas.usuarioRout import usuario_bp
from .rotas.notificacoesRout import  notificacoes_bp

app.register_blueprint(agente_bp)
app.register_blueprint(public_bp)
app.register_blueprint(composicao_bp)
app.register_blueprint(login_bp)
app.register_blueprint(despacho_bp)
app.register_blueprint(gps_bp)
app.register_blueprint(grupodespacho_bp)
app.register_blueprint(instituicao_bp)
app.register_blueprint(json_bp)
app.register_blueprint(ocorrencia_bp)
app.register_blueprint(tipopatrulha_bp)
app.register_blueprint(viatura_bp)
app.register_blueprint(usuariogrupodespacho_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(usuario_bp)
app.register_blueprint(notificacoes_bp)

# print(list(app.url_map.iter_rules()), sep='\n')