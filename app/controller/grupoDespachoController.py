import datetime

from app.forms.grupoDespachoForm import GrupoDespachoForm
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
    @roles_required('MACEIO_ADMIN')
    def listarGrupoDespacho():
        try:
            page = request.args.get('page', 1, type=int)
            
            listGrupoDespacho= GrupoDespacho.query.join(Regional).order_by(Regional.txtRegiao.asc()).paginate(page=page, per_page=ROWS_PER_PAGE)    
            return render_template('grupoDespacho/listarGrupoDespacho.html', listGrupoDespacho=listGrupoDespacho)

        except Exception as e:
            flash('Erro: {}'.format(e), 'error')


    @grupodespacho_bp.route('/prepareCadastrarGrupoDespacho', methods=['GET'])
    @login_required
    @roles_required('MACEIO_ADMIN', 'CAD_DESPACHO')
    def prepareCadastrarGrupoDespacho():

        try:
            form = GrupoDespachoForm(request.form)

            listRegional = Regional.query.order_by(Regional.txtRegiao.asc()).all()
            form.regionais.choices = [(0, "Selecione...")]+[(row.id, row.txtRegiao) for row in listRegional]
            return render_template('grupoDespacho/cadastrarGrupoDespacho.html', form=form)

        except Exception as e:
            flash('Erro: {}'.format(e), 'error')
            return redirect(url_for('usuariogrupodespacho.prepareCadastrarUsuarioGrupoDespacho'))


    @grupodespacho_bp.route('/cadastrarGrupoDespacho' , methods=['POST'])
    @login_required
    @roles_required('MACEIO_ADMIN', 'CAD_DESPACHO')
    def cadastrarGrupoDespacho():

        form = GrupoDespachoForm(request.form)
        dataInicio = datetime.datetime.now()
        try:
            grupoDespacho = GrupoDespacho(None, form.regionais.data , form.nome.data, dataInicio)
            db.session.add(grupoDespacho)
            db.session.commit()
            flash('Grupo de Despacho com sucesso', 'sucess')
            return redirect(url_for('grupodespacho.listarGrupoDespacho'))
        except Exception as e:
            db.session.rollback()
            flash('Erro: {}'.format(e), 'error')
            return redirect(url_for('grupodespacho.listarGrupoDespacho'))               