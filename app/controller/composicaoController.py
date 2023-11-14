import datetime
from operator import and_
from app.forms.composicaoForm import ComposicaoForm
from app.models.viaturaModel import Viatura
from app.models.composicaoModel import Composicao
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
    @roles_required('URBANCAD_AGENTE')
    def listarComposicao():
        try:
            page = request.args.get('page', 1, type=int)
            
            listComposicao = Composicao.query.join(Agente).join(User).filter(and_(User.id == current_user.id, Composicao.dataFim.is_(None))).paginate(page=page, per_page=ROWS_PER_PAGE)    

        except Exception as e:
            flash('Erro: {}'.format(e), 'error')

        return render_template('composicao/listarComposicao.html', listComposicao=listComposicao)

    @composicao_bp.route('/prepareCadastrarComposicao', methods=['GET'])
    @login_required
    @roles_required('URBANCAD_AGENTE')
    def prepareCadastrarComposicao():

        form = ComposicaoForm(request.form)

        listAgente = Agente.query.filter(Agente.dataFim.is_(None)).all()
        form.agente.choices = [(0, "Selecione...")]+[(row.id, row.usuario.name) for row in listAgente]

        listViatura = Viatura.query.filter(Viatura.dataFim.is_(None)).all()
        form.viatura.choices = [(0, "Selecione...")]+[(row.id, row.txtPlaca) for row in listViatura]

        return render_template('composicao/cadastrarComposicao.html', form=form)


    @composicao_bp.route('/cadastrarComposicao' , methods=['POST'])
    @login_required
    @roles_required('URBANCAD_AGENTE')
    def cadastrarComposicao():
        flash('Funcionalidade em DEsenvolvimento', 'error')
        return redirect(url_for('composicao.prepareCadastrarComposicao'))
    #     form = AgenteForm(request.form)
    #     dataInicio = datetime.datetime.now()

    #     try:
    #         agente = Agente(form.instituicao.data, form.usuario.data, dataInicio)
    #         db.session.add(agente)
    #         db.session.commit()
    #         flash('Agente cadastrado com sucesso', 'sucess')
    #         return redirect(url_for('agente.listarAgente'))
    #     except Exception as e:
    #         flash('Erro: {}'.format(e), 'error')
    #         return redirect(url_for('agente.prepareCadastrarAgente'))         