import datetime
from sqlalchemy import and_

from app.models.ocorrenciaHistoricoModel import OcorrenciaHistorico
from app.models.ocorrenciaModel import Ocorrencia
from ..database import db
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from ..enum import statusOcorrenciaEnum
from app.forms.despachoForm import DespachoForm
from app.models.despachoModel import Despacho
from app.models.instituicaoModel import Instituicao
from .roleRequired import roles_required
from ..rotas.despachoRout import despacho_bp

class instituicaoController():

    global ROWS_PER_PAGE 
    ROWS_PER_PAGE = 10

    @roles_required('URBANCAD_ADMIN')
    @despacho_bp.route('/prepareDespachar/<idOcorrencia>', methods=['GET'])
    @login_required
    def prepareDespachar(idOcorrencia):
        form = DespachoForm(request.form)
        form.ocorrencia.data = idOcorrencia
        listInstituicao = Instituicao.query.filter(Instituicao.dataFim.is_(None)).order_by(Instituicao.dataInicio.desc()).all()
        form.despacharPara.choices = [(str(row.id), str(row.txtInstituicao)) for row in listInstituicao]
        return render_template('despacho.html', form=form)
    
    @roles_required('URBANCAD_ADMIN')
    @despacho_bp.route('/despachar', methods=['POST'])
    @login_required
    def despachar():

        try:
            form = DespachoForm(request.form)
            idOcorrencia = form.ocorrencia.data
            listInstituicao = form.despacharPara.data
            datInicio = datetime.datetime.now()

            for row in listInstituicao:
                despacho = Despacho(idOcorrencia, row, current_user.id, datInicio)
                db.session.add(despacho)

            ocorrenciaHistorico = db.session.query(OcorrenciaHistorico).join(Ocorrencia).filter(and_(Ocorrencia.id==idOcorrencia, OcorrenciaHistorico.dataFim.is_(None))).first()
            ocorrenciaHistorico.dataFim = datInicio
          
            newOcorrenciaHistorico = OcorrenciaHistorico(ocorrenciaHistorico.ocorrencia, statusOcorrenciaEnum.StatusOcorrenciaEnum.EM_ANDAMENTO.value, current_user.id, datInicio)
            
            db.session.add(newOcorrenciaHistorico)
            db.session.commit()

        except Exception as e:
            db.session.rollback();
            flash('Erro: {}'.format(e), 'error') 
            return render_template('despacho.html', form=form)

        return redirect(url_for('ocorrencia.prepareSearchOcorrencia'))   
    
    @roles_required('URBANCAD_ADMIN')
    @despacho_bp.route('/prepareSearchDespacho', methods=['GET'])
    @login_required
    def prepareSearchDespacho():
        page = request.args.get('page', 1, type=int)
        listDespacho = Despacho.query.join(Ocorrencia).join(OcorrenciaHistorico).filter(and_(OcorrenciaHistorico.idStatusOcorrencia == statusOcorrenciaEnum.StatusOcorrenciaEnum.EM_ANDAMENTO.value, OcorrenciaHistorico.dataFim.is_(None))).order_by(OcorrenciaHistorico.dataInicio.desc()).paginate(page=page, per_page=ROWS_PER_PAGE)
        return render_template('listarDespacho.html', listDespacho=listDespacho)