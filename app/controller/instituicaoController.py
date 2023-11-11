import datetime
from app.forms.instituicaoForm import InstituicaoForm
from ..database import db
from ..models.instituicaoModel import Instituicao
from ..rotas.instituicaoRout import instituicao_bp
from .roleRequired import roles_required
from flask_login import login_required
from flask import flash, redirect, render_template, request, url_for

class instituicaoController():
        
    global ROWS_PER_PAGE 
    ROWS_PER_PAGE = 10

    @instituicao_bp.route('/prepareSearchInstituicao', methods=['GET'])
    @login_required
    @roles_required('URBANCAD_ADMIN')
    def prepareSearchInstituicao():
        page = request.args.get('page', 1, type=int)
        form = InstituicaoForm(request.form)
        listInstituicao = Instituicao.query.filter(Instituicao.dataFim.is_(None)).order_by(Instituicao.dataInicio.desc()).paginate(page=page, per_page=ROWS_PER_PAGE)
        return render_template('listarInstituicao.html', listInstituicao=listInstituicao, form=form)

    
    @instituicao_bp.route('/prepareCadastrarInstituicao', methods=['GET'])
    @login_required
    @roles_required('URBANCAD_ADMIN')
    def prepareCadastrarInstituicao():
        form = InstituicaoForm(request.form)
        return render_template('cadastrarInstituicao.html', form=form)    
    
    @instituicao_bp.route('/cadastrarInstituicao', methods=['POST'])
    @login_required
    @roles_required('URBANCAD_ADMIN')
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
        
        return redirect(url_for('instituicao.prepareSearchInstituicao'))