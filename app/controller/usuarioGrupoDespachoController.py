import datetime
from app.DAO.grupoDespachoDao import grupoDespachoDao
from app.DAO.userDao import userDao

from app.DAO.usuarioGrupoDespachoDao import usuarioGrupoDespachoDao
from app.enum.rowPerPageEnum import RowPerPageEnum
from app.forms.usuarioGrupoDespachoSearchForm import UsuarioGrupoDespachoSearchForm
from ..database import db
from flask_login import login_required
from app.controller.roleRequired import roles_required
from app.models.grupoDespachoModel import GrupoDespacho
from app.models.userModel import User
from ..models.usuarioGrupoDespachoModel import UsuarioGrupoDespacho
from ..rotas.usuarioGrupoDespachoRout import usuariogrupodespacho_bp
from ..forms.usuarioGrupoDespachoForm import UsuarioGrupoDespachoForm
from flask import render_template, request, redirect, url_for, flash

class UsuarioGrupoDespachoController:    

    global ROWS_PER_PAGE 
    ROWS_PER_PAGE = 10

    @usuariogrupodespacho_bp.route('/listarUsuarioGrupoDespacho', methods=['GET'])
    @login_required
    @roles_required('MACEIO_ADMIN')
    def listar():
        try:
            searchForm = UsuarioGrupoDespachoSearchForm(request.form)
            page = request.args.get('page', 1, type=int)
            searchForm.usuarioSearch.choices = UsuarioGrupoDespachoController.populaUsuario()
            searchForm.grupoDespachoSearch.choices = UsuarioGrupoDespachoController.populaGrupoDespacho()
            
            listUsuarioGrupoDespacho = usuarioGrupoDespachoDao.getListDezUsuarioGrupoDespacho(page)

        except Exception as e:
            flash('Erro: {}'.format(e), 'error')

        return render_template('usuarioGrupoDespacho/listarUsuarioGrupoDespacho.html', listUsuarioGrupoDespacho=listUsuarioGrupoDespacho, searchForm=searchForm, noPagination=True)

    @usuariogrupodespacho_bp.route('/prepareCadastrarUsuarioGrupoDespacho', methods=['GET'])
    @login_required
    @roles_required('MACEIO_ADMIN')
    def prepareCadastrarUsuarioGrupoDespacho():

        try:
            form = UsuarioGrupoDespachoForm(request.form)

            listUsuario = User.query.order_by(User.name.asc()).all()
            form.usuario.choices = [(0, "Selecione...")]+[(row.id, row.name) for row in listUsuario]

            listGrupoDespacho = GrupoDespacho.query.filter(GrupoDespacho.dataFim.is_(None)).order_by(GrupoDespacho.txtNome.asc()).all()
            form.grupoDespacho.choices = [(0, "Selecione...")]+[(row.id, row.txtNome) for row in listGrupoDespacho]
            return render_template('usuarioGrupoDespacho/cadastrarUsuarioGrupoDespacho.html', form=form)

        except Exception as e:
            flash('Erro: {}'.format(e), 'error')
            return redirect(url_for('usuariogrupodespacho.prepareCadastrarUsuarioGrupoDespacho'))


    @usuariogrupodespacho_bp.route('/cadastrarUsuarioGrupoDespacho' , methods=['POST'])
    @login_required
    @roles_required('MACEIO_ADMIN')
    def cadastrarUsuarioGrupoDespacho():

        form = UsuarioGrupoDespachoForm(request.form)
        dataInicio = datetime.datetime.now()
        try:
            usuarioGrupoDespacho = UsuarioGrupoDespacho(form.grupoDespacho.data , form.usuario.data, dataInicio)
            db.session.add(usuarioGrupoDespacho)
            db.session.commit()
            flash('Usuário cadastrado a um Grupo de Despacho com sucesso', 'sucess')
            return redirect(url_for('usuariogrupodespacho.listar'))
        except Exception as e:
            db.session.rollback()
            flash('Erro: {}'.format(e), 'error')
            return redirect(url_for('usuariogrupodespacho.listar'))

    @usuariogrupodespacho_bp.route('/prepareExcluirUsuarioGrupoDespacho/<id>', methods=['GET'])
    @login_required
    @roles_required('MACEIO_ADMIN')
    def prepareExcluir(id):

        usuarioGrupoDespacho = usuarioGrupoDespachoDao.getUsuarioGrupoDespachoById(id)
        form = UsuarioGrupoDespachoForm(request.form, obj=usuarioGrupoDespacho)

        form.usuario.choices = UsuarioGrupoDespachoController.populaUsuario()
        form.grupoDespacho.choices = UsuarioGrupoDespachoController.populaGrupoDespacho()

        for field in form:
            field.flags.disabled = True

        return render_template('usuarioGrupoDespacho/cadastrarUsuarioGrupoDespacho.html', form=form)  

    @usuariogrupodespacho_bp.route('/excluirUsuarioGrupoDespacho/<id>', methods=['GET'])
    @login_required
    @roles_required('MACEIO_ADMIN')
    def excluir(id):
        dataFim = datetime.datetime.now()
        try:
            usuarioGrupoDespachoDao.delete(id, dataFim)
            flash('Usuário excluído com sucesso do Grupo de Despacho', 'sucess')
            return redirect(url_for('usuariogrupodespacho.listar'))
        except Exception as e:
            flash('Erro ao excluir Usuário do Grupo de Despacho', 'error')
            return redirect(url_for('usuariogrupodespacho.prepareExcluir', id=id))

    @usuariogrupodespacho_bp.route('/usuariogrupodespacho.search', methods=['GET'])
    @login_required
    @roles_required('MACEIO_ADMIN')
    def search():
        searchForm = UsuarioGrupoDespachoSearchForm(request.args)
        page = request.args.get('page', 1, type=int)

        querySearch = UsuarioGrupoDespacho.query.join(UsuarioGrupoDespacho.usuario).filter(UsuarioGrupoDespacho.dataFim.is_(None))

        if searchForm.usuarioSearch.data:
            querySearch = querySearch.filter(User.id == searchForm.usuarioSearch.data)            

        if searchForm.grupoDespachoSearch.data:
            querySearch = querySearch.join(UsuarioGrupoDespacho.grupoDespacho).filter(GrupoDespacho.id == searchForm.grupoDespachoSearch.data)

        querySearch = querySearch.order_by(User.name.desc())

        listUsuarioGrupoDespacho = querySearch.paginate(page=page, per_page=RowPerPageEnum.DEZ.value)  

        searchForm.usuarioSearch.choices = UsuarioGrupoDespachoController.populaUsuario()
        searchForm.grupoDespachoSearch.choices = UsuarioGrupoDespachoController.populaGrupoDespacho()

        return render_template('usuarioGrupoDespacho/listarUsuarioGrupoDespacho.html', listUsuarioGrupoDespacho=listUsuarioGrupoDespacho, searchForm=searchForm, noPagination=False)

    @staticmethod
    def populaUsuario():
        listUsuario = userDao.getListUsuario()
        return [(0, "Selecione...")]+[(row.id, row.name) for row in listUsuario]

    @staticmethod
    def populaGrupoDespacho():
        listGrupoDespacho = grupoDespachoDao.getListGrupoDespacho()
        return [(0, "Selecione...")]+[(row.id, row.txtNome) for row in listGrupoDespacho]        
