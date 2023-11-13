import datetime
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
    @roles_required('URBANCAD_ADMIN')
    def listarUsuarioGrupoDespacho():
        try:
            page = request.args.get('page', 1, type=int)
            
            listUsuarioGrupoDespacho= UsuarioGrupoDespacho.query.paginate(page=page, per_page=ROWS_PER_PAGE)    
            return render_template('usuarioGrupoDespacho/listarUsuarioGrupoDespacho.html', listUsuarioGrupoDespacho=listUsuarioGrupoDespacho)

        except Exception as e:
            flash('Erro: {}'.format(e), 'error')


    @usuariogrupodespacho_bp.route('/prepareCadastrarUsuarioGrupoDespacho', methods=['GET'])
    @login_required
    @roles_required('URBANCAD_ADMIN')
    def prepareCadastrarUsuarioGrupoDespacho():

        try:
            form = UsuarioGrupoDespachoForm(request.form)

            listUsuario = User.query.order_by(User.name.asc()).all()
            form.usuarios.choices = [(0, "Selecione...")]+[(row.id, row.name) for row in listUsuario]

            listGrupoDespacho = GrupoDespacho.query.filter(GrupoDespacho.dataFim.is_(None)).order_by(GrupoDespacho.txtNome.asc()).all()
            form.gruposDeDespacho.choices = [(0, "Selecione...")]+[(row.id, row.txtNome) for row in listGrupoDespacho]
            return render_template('usuarioGrupoDespacho/cadastrarUsuarioGrupoDespacho.html', form=form)

        except Exception as e:
            flash('Erro: {}'.format(e), 'error')
            return redirect(url_for('usuariogrupodespacho.prepareCadastrarUsuarioGrupoDespacho'))


    @usuariogrupodespacho_bp.route('/cadastrarUsuarioGrupoDespacho' , methods=['POST'])
    @login_required
    @roles_required('URBANCAD_ADMIN')
    def cadastrarUsuarioGrupoDespacho():

        form = UsuarioGrupoDespachoForm(request.form)
        dataInicio = datetime.datetime.now()
        try:
            usuarioGrupoDespacho = UsuarioGrupoDespacho(form.gruposDeDespacho.data , form.usuarios.data, dataInicio)
            db.session.add(usuarioGrupoDespacho)
            db.session.commit()
            flash('Usuário cadastrado a um Grupo de Despacho com sucesso', 'sucess')
            return redirect(url_for('usuariogrupodespacho.listarUsuarioGrupoDespacho'))
        except Exception as e:
            flash('Erro: {}'.format(e), 'error')
            return redirect(url_for('usuariogrupodespacho.listarUsuarioGrupoDespacho'))               