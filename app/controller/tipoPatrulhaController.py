import datetime

from app.controller.roleRequired import roles_required
from ..database import db
from flask_login import login_required
from ..models.tipoPatrulhaModel import TipoPatrulha
from ..rotas.tipoPatrulhaRout import tipopatrulha_bp
from ..forms.tipoPatrulhaForm import TipoPatrulhaForm
from flask import render_template, request, redirect, url_for, flash

class tipoPatrulhaController:    

    global ROWS_PER_PAGE 
    ROWS_PER_PAGE = 10

    @tipopatrulha_bp.route('/listarTipoPatrulha', methods=['GET'])
    @login_required
    @roles_required('URBANCAD_ADMIN')
    def listarTipoPatrulha():
        try:
            page = request.args.get('page', 1, type=int)
            
            listTipoPatrulha = TipoPatrulha.query.order_by(TipoPatrulha.txtTipoPatrulha.desc()).paginate(page=page, per_page=ROWS_PER_PAGE)    

        except Exception as e:
            flash('Erro: {}'.format(e), 'error')

        return render_template('tipopatrulha/listarTipoPatrulha.html', listTipoPatrulha=listTipoPatrulha)

    @tipopatrulha_bp.route('/prepareCadastrarTipoPatrulha', methods=['GET'])
    @login_required
    @roles_required('URBANCAD_ADMIN')
    def prepareCadastrarTipoPatrulha():

        form = TipoPatrulhaForm(request.form)

        return render_template('tipopatrulha/cadastrarTipoPatrulha.html', form=form)


    @tipopatrulha_bp.route('/cadastrarTipoPatrulha' , methods=['POST'])
    @login_required
    @roles_required('URBANCAD_ADMIN')
    def cadastrarTipoPatrulha():

        form = TipoPatrulhaForm(request.form)
        dataInicio = datetime.datetime.now()

        try:
            tipoPatrulha = TipoPatrulha(form.descricao.data, dataInicio)

            db.session.add(tipoPatrulha)
            db.session.commit()
            flash('Tipo de Patrulha cadastrada com sucesso', 'sucess')
            return redirect(url_for('tipopatrulha.listarTipoPatrulha'))
        except Exception as e:
            db.session.rollback()
            flash('Erro: {}'.format(e), 'error')
            return redirect(url_for('tipopatrulha.prepareCadastrarTipoPatrulha'))               