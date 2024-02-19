import datetime
from app.DAO.tipoPatrulhaDao import tipoPatrulhaDao

from app.controller.roleRequired import roles_required
from app.enum.rowPerPageEnum import RowPerPageEnum
from app.forms.tipoPatrulhaSearchForm import TipoPatrulhaSearchForm
from ..database import db
from flask_login import login_required
from ..models.tipoPatrulhaModel import TipoPatrulha
from ..rotas.tipoPatrulhaRout import tipopatrulha_bp
from ..forms.tipoPatrulhaForm import TipoPatrulhaForm

from flask import render_template, request, redirect, url_for, flash

class tipoPatrulhaController:    

    @tipopatrulha_bp.route('/listarTipoPatrulha', methods=['GET'])
    @login_required
    @roles_required('MACEIO_ADMIN')
    def listar():
        try:
            searchForm = TipoPatrulhaSearchForm(request.form)
            page = request.args.get('page', 1, type=int)
            
            listTipoPatrulha = tipoPatrulhaDao.getListDezTipoPatrulha(page)   

        except Exception as e:
            flash('Erro: {}'.format(e), 'error')

        return render_template('tipopatrulha/listarTipoPatrulha.html', listTipoPatrulha=listTipoPatrulha, searchForm=searchForm, noPagination=True)

    @tipopatrulha_bp.route('/prepareCadastrarTipoPatrulha', methods=['GET'])
    @login_required
    @roles_required('MACEIO_ADMIN')
    def prepareCadastrar():

        form = TipoPatrulhaForm(request.form)

        return render_template('tipopatrulha/cadastrarTipoPatrulha.html', form=form)


    @tipopatrulha_bp.route('/cadastrarTipoPatrulha' , methods=['POST'])
    @login_required
    @roles_required('MACEIO_ADMIN')
    def cadastrarTipoPatrulha():

        form = TipoPatrulhaForm(request.form)
        dataInicio = datetime.datetime.now()

        try:
            tipoPatrulha = TipoPatrulha(form.txtTipoPatrulha.data, dataInicio)

            db.session.add(tipoPatrulha)
            db.session.commit()
            flash('Tipo de Patrulha cadastrada com sucesso', 'sucess')
            return redirect(url_for('tipopatrulha.listar'))
        except Exception as e:
            db.session.rollback()
            flash('Erro: {}'.format(e), 'error')
            return redirect(url_for('tipopatrulha.prepareCadastrar'))

    @tipopatrulha_bp.route('/prepareExcluirTipoPatrulha/<id>', methods=['GET'])
    @login_required
    @roles_required('MACEIO_ADMIN')
    def prepareExcluir(id):

        tipoPatrulha = tipoPatrulhaDao.getTipoPatrulhaById(id)
        form = TipoPatrulhaForm(request.form, obj=tipoPatrulha)

        for field in form:
            field.flags.disabled = True

        return render_template('tipoPatrulha/cadastrarTipoPatrulha.html', form=form)

    @tipopatrulha_bp.route('/excluir/<id>', methods=['GET'])
    @login_required
    @roles_required('MACEIO_ADMIN')
    def excluir(id):
        dataFim = datetime.datetime.now()
        try:
            tipoPatrulhaDao.delete(id, dataFim)
            flash('Tipo de Patrulha excluída com sucesso', 'sucess')
            return redirect(url_for('tipopatrulha.listar'))
        except Exception as e:
            flash('Erro ao excluir Tipo de Patrulha', 'error')
            return redirect(url_for('tipopatrulha.prepareExcluir', id=id))

    @tipopatrulha_bp.route('/searchTipoPatrulha', methods=['GET'])
    @login_required
    @roles_required('MACEIO_ADMIN')
    def search():
        searchForm = TipoPatrulhaSearchForm(request.args)
        page = request.args.get('page', 1, type=int)

        querySearch = TipoPatrulha.query.filter(TipoPatrulha.dataFim.is_(None))

        if searchForm.txtTipoPatrulhaSearch.data:
            querySearch = querySearch.filter(TipoPatrulha.txtTipoPatrulha.ilike('%' + searchForm.txtTipoPatrulhaSearch.data + '%'))

        querySearch = querySearch.order_by(TipoPatrulha.txtTipoPatrulha.desc())

        listTipoPatrulha = querySearch.paginate(page=page, per_page=RowPerPageEnum.DEZ.value)  

        return render_template('tipopatrulha/listarTipoPatrulha.html', listTipoPatrulha=listTipoPatrulha, searchForm=searchForm, noPagination=False)