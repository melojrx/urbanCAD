from app.DAO.despachoDao import DespachoDao
from ..rotas.notificacoesRout import notificacoes_bp
from .roleRequired import roles_required
from flask_login import login_required
from flask import flash, redirect, render_template, session, url_for


class nofificacoesController():


    @notificacoes_bp.route('/notificacoes')
    @login_required
    @roles_required('MACEIO_ADMIN', 'CAD_DESPACHO')
    def notificacoes():
        listOcorrenciaDespachada = None
        if not 'MACEIO_ADMIN' in session["roles"]: 
            listOcorrenciaDespachada = DespachoDao.getListDespachoByUser()
        else:
            listOcorrenciaDespachada = DespachoDao.getListDespachoByAdmin()
        return render_template('notificacoes.html', listOcorrenciaDespachada=listOcorrenciaDespachada)


    @notificacoes_bp.route("/loadListNotificacao",methods=["POST","GET"])
    @login_required
    def loadListNotificacao():

        listOcorrenciaDespachadaCinco = None
        if not 'MACEIO_ADMIN' in session["roles"]: 
            listOcorrenciaDespachadaCinco = DespachoDao.getListDespachoByUser()
        else:
            listOcorrenciaDespachadaCinco = DespachoDao.getListDespachoByAdmin()

        listOcorrenciaDespachadaCinco = listOcorrenciaDespachadaCinco[:5]
        return render_template('loadListNotificacao.html', listOcorrenciaDespachadaCinco=listOcorrenciaDespachadaCinco)