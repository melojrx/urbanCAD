import datetime
import geocoder

from app.forms.ocorrenciaSearchForm import OcorrenciaSearchForm
from ..database import db
from app.models.ocorrenciaModel import Ocorrencia
from app.models.ocorrenciaHistoricoModel import OcorrenciaHistorico
from app.models.subtipoOcorrenciaModel import SubtipoOcorrencia
from app.models.tipoOcorrenciaModel import TipoOcorrencia
from app.models.interessadoModel import Interessado
from ..enum import statusOcorrenciaEnum
from ..rotas.ocorrenciaRout import ocorrencia_bp
from .roleRequired import roles_required
from ..forms.ocorrenciaForm import OcorrenciaForm
from flask_login import login_required, current_user
from sqlalchemy import and_
from flask import flash, jsonify, redirect, render_template, request, session, url_for

class ocorrenciaController():
        
    global ROWS_PER_PAGE 
    ROWS_PER_PAGE = 10

    @ocorrencia_bp.route('/iniciar', methods=['GET'])
    @login_required
    def iniciar():
        try:
            # Se o usário tem permissão de governo
            if 'URBANCAD_GOVERNO' in session["roles"] or 'URBANCAD_ADMIN' in session["roles"]: 
                # Lista todos os eventos cadastrados
                return redirect(url_for('ocorrencia.prepareSearchOcorrencia'))
            else :
                return redirect(url_for('ocorrencia.prepareCadastrarOcorrencia'))

        except Exception as e:
            flash('Erro: {}'.format(e), 'error')

    @roles_required('URBANCAD_ADMIN, URBANCAD_GOVERNO')
    @ocorrencia_bp.route('/prepareSearchOcorrencia', methods=['GET'])
    @login_required
    def prepareSearchOcorrencia():
        page = request.args.get('page', 1, type=int)
        form = OcorrenciaSearchForm(request.form)
        listOcorrenciaHistorico = OcorrenciaHistorico.query.filter(and_(OcorrenciaHistorico.idStatusOcorrencia != statusOcorrenciaEnum.StatusOcorrenciaEnum.FINALIZADO.value, OcorrenciaHistorico.dataFim.is_(None))).order_by(OcorrenciaHistorico.dataInicio.desc()).paginate(page=page, per_page=ROWS_PER_PAGE)
        return render_template('listarOcorrencia.html', listOcorrenciaHistorico=listOcorrenciaHistorico, form=form)


    @roles_required('URBANCAD_ADMIN, URBANCAD_GOVERNO')
    @ocorrencia_bp.route('/searchOcorrencia', methods=['GET'])
    @login_required
    def searchOcorrencia():

        form = OcorrenciaSearchForm(request.form)
        numOcorrenciaSearch = request.args.get('numOcorrenciaSearch')
        form.numOcorrenciaSearch.data = numOcorrenciaSearch
        dataInicioSearch = request.args.get('dataInicioSearch')
        dataFimSearch = request.args.get('dataFimSearch')

        page = request.args.get('page', 1, type=int)

        if dataInicioSearch:
            dataInicioSearch = datetime.datetime.strptime(dataInicioSearch, '%Y-%m-%d')
            form.dataInicioSearch.data = dataInicioSearch
        if dataFimSearch:
            dataFimSearch = datetime.datetime.strptime(dataFimSearch, '%Y-%m-%d')
            dataFimSearch = dataFimSearch.replace(hour=23, minute=59, second=59)
            form.dataFimSearch.data = dataFimSearch

        try: 

            if numOcorrenciaSearch or dataInicioSearch or dataFimSearch:          

                querySearch = OcorrenciaHistorico.query.filter(OcorrenciaHistorico.dataFim.is_(None))

                if numOcorrenciaSearch != "" and numOcorrenciaSearch != None:
                    querySearch= querySearch.join(OcorrenciaHistorico.ocorrencia).filter(Ocorrencia.numOcorrencia == numOcorrenciaSearch)

                if dataInicioSearch and dataFimSearch:
                    querySearch = querySearch.join(OcorrenciaHistorico.ocorrencia).filter(Ocorrencia.dataInicio >= dataInicioSearch).filter(Ocorrencia.dataInicio <= dataFimSearch)
                elif dataInicioSearch and not dataFimSearch:
                    querySearch = querySearch.join(OcorrenciaHistorico.ocorrencia).filter(Ocorrencia.dataInicio >= dataInicioSearch)
                elif not dataInicioSearch and dataFimSearch:
                    querySearch = querySearch.join(OcorrenciaHistorico.ocorrencia).filter(Ocorrencia.dataInicio <= dataFimSearch)

                listOcorrenciaHistorico = querySearch.order_by(OcorrenciaHistorico.dataInicio.desc()).paginate(page=page, per_page=ROWS_PER_PAGE)
            else:
                return redirect(url_for('ocorrencia.prepareSearchOcorrencia'))
   
        except Exception as e:
            flash('Erro: {}'.format(e), 'error')

        return render_template('listarOcorrencia.html', listOcorrenciaHistorico=listOcorrenciaHistorico, form=form)

    @ocorrencia_bp.route('/minhasOcorrencias', methods=['GET'])
    @login_required
    def minhasOcorrencias():
        page = request.args.get('page', 1, type=int)
        listOcorrenciaHistorico = OcorrenciaHistorico.query.filter(and_(OcorrenciaHistorico.idUsuario==current_user.id, OcorrenciaHistorico.dataFim.is_(None))).order_by(OcorrenciaHistorico.dataInicio.desc()).paginate(page=page, per_page=ROWS_PER_PAGE)
        return render_template('minhasOcorrencias.html', listOcorrenciaHistorico=listOcorrenciaHistorico)

    @ocorrencia_bp.route('/prepareCadastrarOcorrencia', methods=['GET'])
    @login_required
    def prepareCadastrarOcorrencia():

        global listTipoOcorrencia 

        form = OcorrenciaForm(request.form)
        listTipoOcorrencia = TipoOcorrencia.query.filter(TipoOcorrencia.dataFim.is_(None)).all()
        form.tipoOcorrencia.choices = [(0, "Selecione...")]+[(row.id, row.txtTipoOcorrencia) for row in listTipoOcorrencia]
        return render_template('cadastrarOcorrencia.html', form=form)    
    
    @ocorrencia_bp.route('/cadastrarOcorrencia', methods=['POST'])
    @login_required
    def cadastrarOcorrencia():

        try:

            form = OcorrenciaForm(request.form)
            
            subtipoOcorrencia = form.subtipoOcorrencia.data
            txtProblema = form.problema.data
            txtEndereco = form.endereco.data
            txtLat = form.latitude.data
            txtLong = form.longitude.data
            txtInteressado = form.txtInteressado.data
            txtCpf = form.txtCpf.data
            txtTelefone = form.txtTelefone.data
            isNoticianteVitima = form.isNoticianteVitima.data
            isNoticianteEstrangeiro = form.isNoticianteEstrangeiro.data
            txtRg = form.txtRg.data
            txtPassaporte = form.txtPassaporte.data
            dataInicio = datetime.datetime.now()

            if not subtipoOcorrencia:
                flash('Informe o subtipo da ocorrência', 'error')
                return render_template('cadastrarOcorrencia.html', listTipoOcorrencia=listTipoOcorrencia, form=form)

            if not txtLat and not txtLong:
                g = geocoder.osm(txtEndereco)

                if not g:
                    flash('Endereço não encontrado', 'error')
                    return render_template('cadastrarOcorrencia.html', listTipoOcorrencia=listTipoOcorrencia, form=form)

                latlong = g.json
                txtLat = latlong['lat']
                txtLong = latlong['lng']

            numOcorrencia = str(dataInicio.year) + str(current_user.id) + str(dataInicio.day) + str(dataInicio.month) + str(dataInicio.hour) + str(dataInicio.minute) + str(dataInicio.second)

            ocorrencia = Ocorrencia(subtipoOcorrencia, current_user.id, numOcorrencia, txtProblema, txtEndereco, txtLat, txtLong, dataInicio)

            ocorrenciaHistorico = OcorrenciaHistorico(ocorrencia, statusOcorrenciaEnum.StatusOcorrenciaEnum.AGUARDANDO_DESPACHO.value, current_user.id, dataInicio)
            interessado = Interessado(ocorrencia, txtInteressado, txtCpf, txtTelefone, isNoticianteVitima, isNoticianteEstrangeiro, txtRg, txtPassaporte)

            db.session.add(ocorrenciaHistorico)
            db.session.add(interessado)
            db.session.commit()

            return redirect(url_for('ocorrencia.iniciar'))
        except Exception as e:
            db.session.rollback()
            flash('Erro: {}'.format(e), 'error')
    
    @ocorrencia_bp.route("/loadSubtipoOcorrencia",methods=["POST","GET"])
    @login_required
    def loadSubtipoOcorrencia():
        form = OcorrenciaForm(request.form)
        if request.method == 'POST':
            id = request.form['id']
            listSubtipoOcorrencia = SubtipoOcorrencia.query.filter(SubtipoOcorrencia.idTipoOcorrencia==id).all()
            form.subtipoOcorrencia.choices = [(0, "Selecione...")]+[(row.id, row.txtSubtipoOcorrencia) for row in listSubtipoOcorrencia]
        return jsonify({'htmlresponse': render_template('loadSubtipoOcorrencia.html', listSubtipoOcorrencia=listSubtipoOcorrencia, form=form)})