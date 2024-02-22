import datetime
from app.DAO.agenteDao import agenteDao
from app.DAO.instituicaoDao import instituicaoDao

from app.controller.roleRequired import roles_required
from app.enum.rowPerPageEnum import RowPerPageEnum
from app.forms.agenteSearchForm import AgenteSearchForm
from app.forms.agenteForm import AgenteForm
from app.models.agenteModel import Agente
from app.models.userModel import User
from ..database import db
from flask_login import login_required
from ..models.instituicaoModel import Instituicao
from ..rotas.agenteRout import agente_bp
from flask import render_template, request, redirect, url_for, flash

class agenteController:    

    @agente_bp.route('/listarAgente', methods=['GET'])
    @login_required
    @roles_required('MACEIO_ADMIN')
    def listar():
        try:
            page = request.args.get('page', 1, type=int)
            searchForm = AgenteSearchForm(request.form)

            listIntituicao = instituicaoDao.getlistInstituicao()
            searchForm.idInstituicaoSearch.choices = [(0, "Selecione...")]+[(ins.id, ins.txtInstituicao) for ins in listIntituicao]
            
            listAgente = agenteDao.getListDezAgentes(page)

        except Exception as e:
            flash('Erro: {}'.format(e), 'error')

        return render_template('agente/listarAgente.html', listAgente=listAgente, searchForm=searchForm, noPagination=True)

    @agente_bp.route('/prepareCadastrarAgente', methods=['GET'])
    @login_required
    @roles_required('MACEIO_ADMIN')
    def prepareCadastrar():

        form = AgenteForm(request.form)

        listUsuario = User.query.all()
        form.usuario.choices = [(0, "Selecione...")]+[(row.id, row.name) for row in listUsuario]

        listIntituicao = Instituicao.query.filter(Instituicao.dataFim.is_(None)).all()
        form.idInstituicao.choices = [(0, "Selecione...")]+[(row.id, row.txtInstituicao) for row in listIntituicao]

        return render_template('agente/cadastrarAgente.html', form=form)


    @agente_bp.route('/cadastrarAgente' , methods=['POST'])
    @login_required
    @roles_required('MACEIO_ADMIN')
    def cadastrarAgente():

        form = AgenteForm(request.form)
        dataInicio = datetime.datetime.now()

        try:
            agente = Agente(form.idInstituicao.data, form.usuario.data, dataInicio)
            db.session.add(agente)
            db.session.commit()
            flash('Agente cadastrado com sucesso', 'sucess')
            return redirect(url_for('agente.listar'))
        except Exception as e:
            db.session.rollback()
            flash('Erro: {}'.format(e), 'error')
            return redirect(url_for('agente.prepareCadastrarAgente'))

    @agente_bp.route('/prepareExcluirAgente/<id>', methods=['GET'])
    @login_required
    @roles_required('MACEIO_ADMIN')
    def prepareExcluir(id):

        agente = agenteDao.getAgenteById(id)

        form = AgenteForm(request.form, obj=agente)

        listUsuario = User.query.all()
        form.usuario.choices = [(0, "Selecione...")]+[(row.id, row.name) for row in listUsuario]
        listIntituicao = instituicaoDao.getlistInstituicao()
        form.idInstituicao.choices = [(0, "Selecione...")]+[(ins.id, ins.txtInstituicao) for ins in listIntituicao]
    
        for field in form:
            field.flags.disabled = True

        return render_template('agente/cadastrarAgente.html', form=form)
    
    @agente_bp.route('/excluirAgente/<id>', methods=['GET'])
    @login_required
    @roles_required('MACEIO_ADMIN')
    def excluir(id):
        dataFim = datetime.datetime.now()
        try:
            agenteDao.delete(id, dataFim)
            flash('Agente excluído com sucesso', 'sucess')
            return redirect(url_for('agente.listar'))
        except Exception as e:
            flash('Erro ao excluir agente', 'error')
            return redirect(url_for('agente.prepareExcluir', id=id))

    @agente_bp.route('/search', methods=['GET'])
    @login_required
    @roles_required('MACEIO_ADMIN')
    def search():
        searchForm = AgenteSearchForm(request.args)
        page = request.args.get('page', 1, type=int)

        querySearch = Agente.query.filter(Agente.dataFim.is_(None))

        if searchForm.idInstituicaoSearch.data:
            querySearch = querySearch.join(Instituicao).filter(Instituicao.id == searchForm.idInstituicaoSearch.data)           

        if searchForm.agenteSearch.data:
            querySearch = querySearch.join(User).filter(User.name.ilike('%' + searchForm.agenteSearch.data + '%'))

        querySearch = querySearch.order_by(Agente.dataInicio.asc())

        listAgente = querySearch.paginate(page=page, per_page=RowPerPageEnum.DEZ.value)  

        listIntituicao = instituicaoDao.getlistInstituicao()
        searchForm.idInstituicaoSearch.choices = [(0, "Selecione...")]+[(ins.id, ins.txtInstituicao) for ins in listIntituicao]

        return render_template('agente/listarAgente.html', listAgente=listAgente, searchForm=searchForm, noPagination=False)    