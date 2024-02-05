import datetime
from operator import and_
from app.forms.composicaoForm import ComposicaoForm
from app.models.composicaoViaturaModel import ComposicaoViatura
from app.models.viaturaModel import Viatura
from app.controller.roleRequired import roles_required
from app.models.agenteModel import Agente
from app.models.userModel import User
from ..database import db
from flask_login import current_user, login_required
from ..rotas.composicaoRout import composicao_bp
from flask import render_template, request, redirect, url_for, flash

class composicaoController:    

    global ROWS_PER_PAGE 
    ROWS_PER_PAGE = 10

    @composicao_bp.route('/listarComposicao', methods=['GET'])
    @login_required
    @roles_required('CAD_AGENTE')
    def listarComposicao():
        try:
            page = request.args.get('page', 1, type=int)
            
            listComposicao = ComposicaoViatura.query.join(Agente).join(User).filter(and_(User.id == current_user.id, ComposicaoViatura.dataFim.is_(None))).paginate(page=page, per_page=ROWS_PER_PAGE)    

        except Exception as e:
            flash('Erro: {}'.format(e), 'error')

        return render_template('composicao/listarComposicao.html', listComposicao=listComposicao)

    @composicao_bp.route('/prepareCadastrarComposicao', methods=['GET'])
    @login_required
    @roles_required('CAD_AGENTE')
    def prepareCadastrarComposicao():

        form = ComposicaoForm(request.form)

        listAgente = Agente.query.filter(Agente.dataFim.is_(None)).all()
        form.agente.choices = [(0, "Selecione...")]+[(row.id, row.usuario.name) for row in listAgente]

        listViatura = Viatura.query.filter(Viatura.dataFim.is_(None)).all()
        form.viatura.choices = [(0, "Selecione...")]+[(row.id, row) for row in listViatura]

        return render_template('composicao/cadastrarComposicao.html', form=form)


    @composicao_bp.route('/cadastrarComposicao' , methods=['POST'])
    @login_required
    @roles_required('CAD_AGENTE')
    def cadastrarComposicao():

        form = ComposicaoForm(request.form)
        dataInicio = datetime.datetime.now()

        try:
            composicaoViatura = ComposicaoViatura(form.viatura.data, form.agente.data, dataInicio)
            # composicao = Composicao(composicaoViatura, form.agente.data, dataInicio)

            db.session.add(composicaoViatura)
            db.session.commit()
            flash('Composição cadastrada com sucesso', 'sucess')
            return redirect(url_for('composicao.listarComposicao'))
        except Exception as e:
            db.session.rollback()
            flash('Erro: {}'.format(e), 'error')
            return redirect(url_for('composicao.prepareCadastrarComposicao'))

    @composicao_bp.route('/prepareFinalizarComposicao/<idComposicaoViatura>' , methods=['GET'])
    @login_required
    @roles_required('CAD_AGENTE')
    def prepareFinalizarComposicao(idComposicaoViatura):
        try:
            composicaoViatura = ComposicaoViatura.query.filter(ComposicaoViatura.id == idComposicaoViatura).first()
            return render_template('composicao/finalizarComposicao.html', composicaoViatura=composicaoViatura)
        except Exception as e:
            db.session.rollback()
            flash('Erro: {}'.format(e), 'error')
            return redirect(url_for('composicao.listarComposicao'))

    @composicao_bp.route('/finalizarComposicao/<idComposicaoViatura>' , methods=['GET'])
    @login_required
    @roles_required('CAD_AGENTE')
    def finalizarComposicao(idComposicaoViatura):
        try:
            dataInicio = datetime.datetime.now()

            composicaoViatura = ComposicaoViatura.query.filter(ComposicaoViatura.id == idComposicaoViatura).first()
            composicaoViatura.dataFim = dataInicio

            db.session.add(composicaoViatura)
            db.session.commit()

            flash('Composição finalizada com sucesso', 'sucess')
            return redirect(url_for('composicao.listarComposicao'))
        except Exception as e:
            db.session.rollback()
            flash('Erro: {}'.format(e), 'error')
            return redirect(url_for('composicao.listarComposicao'))                   