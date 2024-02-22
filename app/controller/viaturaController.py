import datetime
from app.DAO.instituicaoDao import instituicaoDao
from app.DAO.tipoPatrulhaDao import tipoPatrulhaDao
from app.DAO.viaturaDao import viaturaDao

from app.controller.roleRequired import roles_required
from app.enum.rowPerPageEnum import RowPerPageEnum
from app.forms.viaturaSearchForm import ViaturaSearchForm
from app.models.instituicaoModel import Instituicao
from app.models.tipoPatrulhaModel import TipoPatrulha
from ..database import db
from flask_login import login_required
from ..models.viaturaModel import Viatura
from ..rotas.viaturaRout import viatura_bp
from ..forms.viaturaForm import ViaturaForm
from flask import render_template, request, redirect, url_for, flash

class viaturaController():    

    @viatura_bp.route('/listarViaturas', methods=['GET'])
    @login_required
    @roles_required('MACEIO_ADMIN')
    def listar():
        try:
            searchForm = ViaturaSearchForm(request.form)
            page = request.args.get('page', 1, type=int)

            listIntituicao = instituicaoDao.getlistInstituicao()
            searchForm.idInstituicaoSearch.choices = [(0, "Selecione...")]+[(ins.id, ins.txtInstituicao) for ins in listIntituicao]
            listTipoPatrulha = tipoPatrulhaDao.getlistTipoPatrulha()
            searchForm.idTipoPatrulhaSearch.choices = [(0, "Selecione...")]+[(tpa.id, tpa.txtTipoPatrulha) for tpa in listTipoPatrulha] 

            listViatura = viaturaDao.getListDezViaturas(page)    

        except Exception as e:
            flash('Erro: {}'.format(e), 'error')

        return render_template('viatura/listarViatura.html', listViatura=listViatura, searchForm=searchForm, noPagination=True)

    @viatura_bp.route('/prepareCadastrar', methods=['GET'])
    @login_required
    @roles_required('MACEIO_ADMIN')
    def prepareCadastrar():
        form = ViaturaForm(data=request.args)

        form.idInstituicao.choices = viaturaController.populaInstituicao()
        form.idTipoPatrulha.choices = viaturaController.populaTipoPatrulha()

        return render_template('viatura/cadastrarViatura.html', form=form)


    @viatura_bp.route('/cadastrar' , methods=['POST'])
    @login_required
    @roles_required('MACEIO_ADMIN')
    def cadastrar():

        form = ViaturaForm(request.form)

        tipoPatrulha = form.idTipoPatrulha.data
        instituicao = form.idInstituicao.data

        if(tipoPatrulha == 0):
            flash('Informe o Tipo de Patrulha', 'error')
            return redirect(url_for('viatura.prepareCadastrar', **form.data))
        if(instituicao == 0):
            flash('Informe a Instituição', 'error')
            return redirect(url_for('viatura.prepareCadastrar', **form.data))

        try:
            dataInicio = datetime.datetime.now()
            viatura = Viatura(instituicao, tipoPatrulha, form.txtCodigo.data.upper(), form.txtPlaca.data.upper(),form.txtDescricao.data, dataInicio)
            db.session.add(viatura)
            db.session.commit()
            flash('Viatura cadastrada com sucesso', 'sucess')
            return redirect(url_for('viatura.listar')) 
        except Exception as e:
            db.session.rollback()
            flash('Erro: {}'.format(e), 'error')
            return redirect(url_for('viatura.prepareCadastrar'))


    @viatura_bp.route('/prepareExcluirViatura/<id>', methods=['GET'])
    @login_required
    @roles_required('MACEIO_ADMIN')
    def prepareExcluir(id):

        viatura = viaturaDao.getViaturaById(id)
        form = ViaturaForm(request.form, obj=viatura)

        form.idInstituicao.choices = viaturaController.populaInstituicao()
        form.idTipoPatrulha.choices = viaturaController.populaTipoPatrulha()     

        for field in form:
            field.flags.disabled = True

        return render_template('viatura/cadastrarViatura.html', form=form)
    

    @viatura_bp.route('/excluirViatura/<id>', methods=['GET'])
    @login_required
    @roles_required('MACEIO_ADMIN')
    def excluir(id):
        dataFim = datetime.datetime.now()
        try:
            viaturaDao.delete(id, dataFim)
            flash('Viatura excluída com sucesso', 'sucess')
            return redirect(url_for('viatura.listar'))
        except Exception as e:
            flash('Erro ao excluir viatura', 'error')
            return redirect(url_for('viatura.prepareExcluir', id=id))
        
    @viatura_bp.route('/viatura.searchViatura', methods=['GET'])
    @login_required
    @roles_required('MACEIO_ADMIN')
    def search():
        searchForm = ViaturaSearchForm(request.args)
        page = request.args.get('page', 1, type=int)

        querySearch = Viatura.query.filter(Viatura.dataFim.is_(None))

        if searchForm.idInstituicaoSearch.data:
            querySearch = querySearch.join(Viatura.instituicao).filter(Instituicao.id == searchForm.idInstituicaoSearch.data)            

        if searchForm.idTipoPatrulhaSearch.data:
            querySearch = querySearch.join(Viatura.tipoPatrulha).filter(TipoPatrulha.id == searchForm.idTipoPatrulhaSearch.data)

        if searchForm.txtCodigoSearch.data:
            querySearch = querySearch.filter(Viatura.txtCodigo == searchForm.txtCodigoSearch.data.upper())

        if searchForm.txtPlacaSearch.data:
            querySearch = querySearch.filter(Viatura.txtPlaca == searchForm.txtPlacaSearch.data.upper())

        querySearch = querySearch.order_by(Viatura.txtCodigo.desc())

        listViatura = querySearch.paginate(page=page, per_page=RowPerPageEnum.DEZ.value)  

        searchForm.idInstituicaoSearch.choices = viaturaController.populaInstituicao()
        searchForm.idTipoPatrulhaSearch.choices = viaturaController.populaTipoPatrulha()

        return render_template('viatura/listarViatura.html', listViatura=listViatura, searchForm=searchForm, noPagination=False)
    
    @staticmethod
    def populaTipoPatrulha():
        listTipoPatrulha = tipoPatrulhaDao.getlistTipoPatrulha()
        return ([(0, "Selecione...")]+[(row.id, row.txtTipoPatrulha) for row in listTipoPatrulha])

    @staticmethod
    def populaInstituicao():
        listIntituicao = instituicaoDao.getlistInstituicao()
        return ([(0, "Selecione...")]+[(row.id, row.txtInstituicao) for row in listIntituicao])           
