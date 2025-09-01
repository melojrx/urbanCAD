import datetime
from app.DAO.grupoDespachoDao import grupoDespachoDao
from app.DAO.regionalDao import regionalDao
from app.enum.rowPerPageEnum import RowPerPageEnum

from app.forms.grupoDespachoForm import GrupoDespachoForm
from app.forms.grupoDespachoSearchForm import GrupoDespachoSearchForm
from app.models.regionaisModel import Regional
from ..database import db
from flask_login import login_required
from app.controller.roleRequired import roles_required
from app.models.grupoDespachoModel import GrupoDespacho
from app.models.userModel import User
from ..rotas.grupoDespachoRout import grupodespacho_bp
from flask import render_template, request, redirect, url_for, flash

class GrupoDespachoController:    

    global ROWS_PER_PAGE 
    ROWS_PER_PAGE = 10

    @grupodespacho_bp.route('/listarGrupoDespacho', methods=['GET'])
    @login_required
    @roles_required('CAD_ADMIN', 'CAD_DESPACHO')
    def listar():
        try:
            searchForm = GrupoDespachoSearchForm(request.form)
            page = request.args.get('page', 1, type=int)
            searchForm.idRegionalSearch.choices = GrupoDespachoController.populaRegionais()

            listGrupoDespacho = grupoDespachoDao.getListDezGrupoDespacho(page)

        except Exception as e:
            flash('Erro: {}'.format(e), 'error')

        return render_template('grupoDespacho/listarGrupoDespacho.html', listGrupoDespacho=listGrupoDespacho, searchForm=searchForm, noPagination=True)

    @grupodespacho_bp.route('/prepareCadastrarGrupoDespacho', methods=['GET'])
    @login_required
    @roles_required('CAD_ADMIN', 'CAD_DESPACHO')
    def prepareCadastrarGrupoDespacho():

        try:
            form = GrupoDespachoForm(data=request.args)
            
            form.idRegional.choices = GrupoDespachoController.populaRegionais()
            return render_template('grupoDespacho/cadastrarGrupoDespacho.html', form=form)

        except Exception as e:
            flash('Erro: {}'.format(e), 'error')
            return redirect(url_for('grupodespacho.listar'))


    @grupodespacho_bp.route('/cadastrarGrupoDespacho' , methods=['POST'])
    @login_required
    @roles_required('CAD_ADMIN', 'CAD_DESPACHO')
    def cadastrarGrupoDespacho():

        form = GrupoDespachoForm(request.form)

        idRegional = form.idRegional.data

        if(idRegional == 0):
            flash('Informe a Regional', 'error')
            return redirect(url_for('grupodespacho.prepareCadastrarGrupoDespacho', **form.data))

        try:
            dataInicio = datetime.datetime.now()
            grupoDespacho = GrupoDespacho(None,  idRegional, form.txtNome.data, dataInicio)
            db.session.add(grupoDespacho)
            db.session.commit()
            flash('Grupo de Despacho com sucesso', 'sucess')
            return redirect(url_for('grupodespacho.listar'))
        except Exception as e:
            db.session.rollback()
            flash('Erro: {}'.format(e), 'error')
            return redirect(url_for('grupodespacho.listar'))

    @grupodespacho_bp.route('/prepareExcluirGrupoDespacho/<id>', methods=['GET'])
    @login_required
    @roles_required('CAD_ADMIN')
    def prepareExcluir(id):

        grupoDespacho = grupoDespachoDao.getGrupoDespachoById(id)
        form = GrupoDespachoForm(request.form, obj=grupoDespacho)
        form.idRegional.choices = GrupoDespachoController.populaRegionais()

        for field in form:
            field.flags.disabled = True

        return render_template('grupoDespacho/cadastrarGrupoDespacho.html', form=form) 

    @grupodespacho_bp.route('/excluirGrupoDespacho/<id>', methods=['GET'])
    @login_required
    @roles_required('CAD_ADMIN')
    def excluir(id):
        dataFim = datetime.datetime.now()
        try:
            grupoDespachoDao.delete(id, dataFim)
            flash('Grupo de despacho excluído com sucesso', 'sucess')
            return redirect(url_for('grupodespacho.listar'))
        except Exception as e:
            flash('Erro ao excluir Grupo de despacho', 'error')
            return redirect(url_for('grupodespacho.prepareExcluir', id=id))

    @grupodespacho_bp.route('/viatura.search', methods=['GET'])
    @login_required
    @roles_required('CAD_ADMIN')
    def search():
        searchForm = GrupoDespachoSearchForm(request.args)
        page = request.args.get('page', 1, type=int)

        querySearch = GrupoDespacho.query.filter(GrupoDespacho.dataFim.is_(None))

        if searchForm.txtNomeSearch.data:        
            querySearch = querySearch.filter(GrupoDespacho.txtNome.ilike('%' + searchForm.txtNomeSearch.data + '%'))

        if searchForm.idRegionalSearch.data:
            querySearch = querySearch.join(GrupoDespacho.regional).filter(Regional.id == searchForm.idRegionalSearch.data)

        querySearch = querySearch.order_by(GrupoDespacho.txtNome.asc())

        listGrupoDespacho = querySearch.paginate(page=page, per_page=RowPerPageEnum.DEZ.value)  

        searchForm.idRegionalSearch.choices = GrupoDespachoController.populaRegionais()

        return render_template('grupoDespacho/listarGrupoDespacho.html', listGrupoDespacho=listGrupoDespacho, searchForm=searchForm, noPagination=False)

    @staticmethod
    def populaRegionais():
        listRegional = regionalDao.getListRegionais()
        return [(0, "Selecione...")]+[(row.id, row.txtRegiao) for row in listRegional]