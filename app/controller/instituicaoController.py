import datetime
from app.DAO.instituicaoDao import instituicaoDao
from app.enum.rowPerPageEnum import RowPerPageEnum
from app.forms.instituicaoForm import InstituicaoForm
from app.forms.instituicaoSearchForm import InstituicaoSearchForm
from ..database import db
from ..models.instituicaoModel import Instituicao
from ..rotas.instituicaoRout import instituicao_bp
from .roleRequired import roles_required
from flask_login import login_required
from flask import flash, redirect, render_template, request, url_for

class instituicaoController():
        
    global ROWS_PER_PAGE 
    ROWS_PER_PAGE = 10

    @instituicao_bp.route('/listarInstituicao', methods=['GET'])
    @login_required
    @roles_required('MACEIO_ADMIN')
    def listar():
        page = request.args.get('page', 1, type=int)
        searchForm = InstituicaoSearchForm(request.form)
        listInstituicao = instituicaoDao.getListDezInstituicoes(page)
        return render_template('instituicao/listarInstituicao.html', listInstituicao=listInstituicao, searchForm=searchForm, noPagination=True)

    
    @instituicao_bp.route('/prepareCadastrarInstituicao', methods=['GET'])
    @login_required
    @roles_required('MACEIO_ADMIN')
    def prepareCadastrar():
        form = InstituicaoForm(request.form)
        return render_template('instituicao/cadastrarInstituicao.html', form=form)    
    
    @instituicao_bp.route('/cadastrarInstituicao', methods=['POST'])
    @login_required
    @roles_required('MACEIO_ADMIN')
    def cadastrarInstituicao():

        try:

            form = InstituicaoForm(request.form)
            
            txtInstituicao = form.txtInstituicao.data
            txtSigla = form.txtSigla.data
            dataInicio = datetime.datetime.now()

            instutuicao = Instituicao(txtInstituicao, txtSigla, dataInicio)
            
            db.session.add(instutuicao)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            flash('Erro: {}'.format(e), 'error')      
        
        return redirect(url_for('instituicao.listar'))
    
    @instituicao_bp.route('/prepareExcluirInstituicao/<id>', methods=['GET'])
    @login_required
    @roles_required('MACEIO_ADMIN')
    def prepareExcluir(id):

        viatura = instituicaoDao.getInstituicaoById(id)
        form = InstituicaoForm(request.form, obj=viatura)

        for field in form:
            field.flags.disabled = True

        return render_template('instituicao/cadastrarInstituicao.html', form=form)
    
    @instituicao_bp.route('/excluir/<id>', methods=['GET'])
    @login_required
    @roles_required('MACEIO_ADMIN')
    def excluir(id):
        dataFim = datetime.datetime.now()
        try:
            instituicaoDao.delete(id, dataFim)
            flash('Instituição excluída com sucesso', 'sucess')
            return redirect(url_for('instituicao.listar'))
        except Exception as e:
            flash('Erro ao excluir Instituição', 'error')
            return redirect(url_for('instituicao.prepareExcluir', id=id))

    @instituicao_bp.route('/searchInstituicao', methods=['GET'])
    @login_required
    @roles_required('MACEIO_ADMIN')
    def search():
        searchForm = InstituicaoSearchForm(request.args)
        page = request.args.get('page', 1, type=int)

        querySearch = Instituicao.query.filter(Instituicao.dataFim.is_(None))

        if searchForm.txtInstituicaoSearch.data:
            querySearch = querySearch.filter(Instituicao.txtInstituicao.ilike('%' + searchForm.txtInstituicaoSearch.data + '%'))      

        if searchForm.txtSiglaSearch.data:
            querySearch = querySearch.filter(Instituicao.txtSigla.ilike('%' + searchForm.txtSiglaSearch.data + '%'))

        querySearch = querySearch.order_by(Instituicao.txtInstituicao.desc())

        listInstituicao = querySearch.paginate(page=page, per_page=RowPerPageEnum.DEZ.value)  

        return render_template('instituicao/listarInstituicao.html', listInstituicao=listInstituicao, searchForm=searchForm, noPagination=False)           