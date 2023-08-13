import datetime
from ..database import db
from flask_login import login_required
from ..models.viaturaModel import Viatura
from ..models.instituicaoModel import Instituicao
from ..models.tipoPatrulhaModel import TipoPatrulha
from ..rotas.viaturaRout import viatura_bp
from ..forms.viaturaForm import ViaturaForm
from flask import render_template, request, redirect, url_for, flash

class viaturaController:    

    global ROWS_PER_PAGE 
    ROWS_PER_PAGE = 5

    @viatura_bp.route('/listarViaturas', methods=['GET'])
    # @login_required
    def listarViaturas():
        try:
            page = request.args.get('page', 1, type=int)
            
            listViatura = Viatura.query.order_by(Viatura.txtCodigo.desc()).paginate(page=page, per_page=ROWS_PER_PAGE)    

        except Exception as e:
            flash('Erro: {}'.format(e), 'error')

        return render_template('viatura/listarViatura.html', listViatura=listViatura)

    @viatura_bp.route('/prepareCadastrar', methods=['GET'])
    @login_required
    def prepareCadastrar():
        form = ViaturaForm(request.form)

        listIntituicao = Instituicao.query.filter(Instituicao.dataFim.is_(None)).all()
        form.instituicao.choices = [(0, "Selecione...")]+[(ins.id, ins.txtInstituicao) for ins in listIntituicao]

        listTipoPatrulha = TipoPatrulha.query.filter(TipoPatrulha.dataFim.is_(None)).all()
        form.tipoPatrulha.choices = [(0, "Selecione...")]+[(tpa.id, tpa.txtTipoPatrulha) for tpa in listTipoPatrulha]

        return render_template('viatura/cadastrarViatura.html', form=form)


    @viatura_bp.route('/cadastrar' , methods=['POST'])
    @login_required
    def cadastrar():

        form = ViaturaForm(request.form)
        dataInicio = datetime.datetime.now()

        viatura = Viatura(form.instituicao.data, form.tipoPatrulha.data, form.codigo.data, form.placa.data,form.descricao.data, dataInicio)
        db.session.add(viatura)
        db.session.commit()
        flash('Viatura cadastrada com sucesso', 'sucess')
        return redirect(url_for('viatura.listarViaturas'))        