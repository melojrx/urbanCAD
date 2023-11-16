import datetime

from app.controller.roleRequired import roles_required
from app.forms.agenteForm import AgenteForm
from app.models.agenteModel import Agente
from app.models.userModel import User
from ..database import db
from flask_login import login_required
from ..models.instituicaoModel import Instituicao
from ..rotas.agenteRout import agente_bp
from flask import render_template, request, redirect, url_for, flash

class agenteController:    

    global ROWS_PER_PAGE 
    ROWS_PER_PAGE = 10

    @agente_bp.route('/listarAgente', methods=['GET'])
    @login_required
    @roles_required('URBANCAD_ADMIN')
    def listarAgente():
        try:
            page = request.args.get('page', 1, type=int)
            
            listAgente = Agente.query.paginate(page=page, per_page=ROWS_PER_PAGE)    

        except Exception as e:
            flash('Erro: {}'.format(e), 'error')

        return render_template('agente/listarAgente.html', listAgente=listAgente)

    @agente_bp.route('/prepareCadastrarAgente', methods=['GET'])
    @login_required
    @roles_required('URBANCAD_ADMIN')
    def prepareCadastrarAgente():

        form = AgenteForm(request.form)

        listUsuario = User.query.all()
        form.usuario.choices = [(0, "Selecione...")]+[(row.id, row.name) for row in listUsuario]

        listIntituicao = Instituicao.query.filter(Instituicao.dataFim.is_(None)).all()
        form.instituicao.choices = [(0, "Selecione...")]+[(row.id, row.txtInstituicao) for row in listIntituicao]

        return render_template('agente/cadastrarAgente.html', form=form)


    @agente_bp.route('/cadastrarAgente' , methods=['POST'])
    @login_required
    @roles_required('URBANCAD_ADMIN')
    def cadastrarAgente():

        form = AgenteForm(request.form)
        dataInicio = datetime.datetime.now()

        try:
            agente = Agente(form.instituicao.data, form.usuario.data, dataInicio)
            db.session.add(agente)
            db.session.commit()
            flash('Agente cadastrado com sucesso', 'sucess')
            return redirect(url_for('agente.listarAgente'))
        except Exception as e:
            db.session.rollback()
            flash('Erro: {}'.format(e), 'error')
            return redirect(url_for('agente.prepareCadastrarAgente'))         