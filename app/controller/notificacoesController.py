from ..rotas.notificacoesRout import notificacoes_bp
from .roleRequired import roles_required
from flask_login import login_required
from flask import flash, redirect, render_template, url_for


class nofificacoesController():

    global ROWS_PER_PAGE
    ROWS_PER_PAGE = 10

    @notificacoes_bp.route('/notificacoes')
    @login_required
    @roles_required('MACEIO_ADMIN', 'CAD_DESPACHO')
    def notificacoes():
        return render_template('notificacoes.html')
