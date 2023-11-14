import datetime
from sqlalchemy import and_

from app.models.grupoDespachoModel import GrupoDespacho
from app.models.userModel import User
from app.models.usuarioGrupoDespachoModel import UsuarioGrupoDespacho

from ..database import db
from flask import flash, redirect, render_template, request, session, url_for
from flask_login import login_required, current_user
from ..enum import statusOcorrenciaEnum
from ..enum import statusDespachoEnum
from app.forms.despachoForm import DespachoForm
from app.models.despachoModel import Despacho
from app.models.ocorrenciaHistoricoModel import OcorrenciaHistorico
from app.models.ocorrenciaGrupoDespachoModel import OcorrenciaGrupoDespacho
from app.models.ocorrenciaModel import Ocorrencia
from app.models.despachoHistoricoModel import DespachoHistorico
from app.models.viaturaModel import Viatura
from .roleRequired import roles_required
from ..rotas.despachoRout import despacho_bp

class DespachoController():

    global ROWS_PER_PAGE 
    ROWS_PER_PAGE = 10

    @despacho_bp.route('/prepareSearchDespacho', methods=['GET'])
    @login_required
    @roles_required('URBANCAD_ADMIN', 'URBANCAD_GOVERNO', 'URBANCAD_DESPACHO')
    def prepareSearchDespacho():

        page = request.args.get('page', 1, type=int)
        
        querySearchDespacho = None
        querySearchADespachar = None

        if not 'URBANCAD_ADMIN' in session["roles"]:    
            querySearchDespacho = (Despacho.query.join(Ocorrencia)
                        .join(OcorrenciaHistorico)
                        .join(OcorrenciaGrupoDespacho).join(User)
                        .filter(
                            OcorrenciaHistorico.idStatusOcorrencia == statusOcorrenciaEnum.StatusOcorrenciaEnum.EM_ANDAMENTO.value, 
                            User.id == current_user.id,
                            OcorrenciaHistorico.dataFim.is_(None))
                        )

            querySearchADespachar = (OcorrenciaHistorico.query
                .join(Ocorrencia)
                .outerjoin(Despacho, Despacho.idOcorrencia == Ocorrencia.id)
                .join(OcorrenciaGrupoDespacho)
                .join(GrupoDespacho)
                .join(UsuarioGrupoDespacho)
                .filter(
                    OcorrenciaHistorico.dataFim.is_(None),
                    Despacho.id.is_(None),
                    UsuarioGrupoDespacho.idUsuario == current_user.id
                )
            )
        else:
            querySearchDespacho = (Despacho.query.join(Ocorrencia)
                        .join(OcorrenciaHistorico)
                        .filter(
                            OcorrenciaHistorico.idStatusOcorrencia == statusOcorrenciaEnum.StatusOcorrenciaEnum.EM_ANDAMENTO.value, 
                            OcorrenciaHistorico.dataFim.is_(None))
                        )

            querySearchADespachar = (OcorrenciaHistorico.query
                .join(Ocorrencia)
                .outerjoin(Despacho, Despacho.idOcorrencia == Ocorrencia.id)
                .filter(
                    OcorrenciaHistorico.dataFim.is_(None),
                    Despacho.id.is_(None)
                    )
            )

            

        listDespacho = querySearchDespacho.order_by(OcorrenciaHistorico.dataInicio.desc()).paginate(page=page, per_page=ROWS_PER_PAGE)                   
        listDespachar = querySearchADespachar.order_by(OcorrenciaHistorico.dataInicio.desc()).paginate(page=page, per_page=ROWS_PER_PAGE)


        return render_template('listarDespacho.html', listDespacho=listDespacho, listDespachar=listDespachar)

    @despacho_bp.route('/prepareDespachar/<idOcorrencia>', methods=['GET'])
    @login_required
    @roles_required('URBANCAD_ADMIN', 'URBANCAD_GOVERNO', 'URBANCAD_DESPACHO')    
    def prepareDespachar(idOcorrencia):
        form = DespachoForm(request.form)
        form.ocorrencia.data = idOcorrencia
        listViatura = Viatura.query.filter(Viatura.dataFim.is_(None)).all()
        form.despacharPara.choices = [(str(row.id), str(row.instituicao.txtSigla)
                                      + " - " + str(row.tipoPatrulha.txtTipoPatrulha)
                                      + " " + str(row.txtDescricao)
                                      + " " + str(row.txtCodigo)
                                      + " " + str(row.txtPlaca)
                                       ) for row in listViatura]
        return render_template('despacho.html', form=form)

    @despacho_bp.route('/despachar', methods=['POST'])
    @login_required
    @roles_required('URBANCAD_ADMIN', 'URBANCAD_GOVERNO', 'URBANCAD_DESPACHO')    
    def despachar():

        try:
            form = DespachoForm(request.form)
            idOcorrencia = form.ocorrencia.data
            listViatura = form.despacharPara.data
            datInicio = datetime.datetime.now()

            for row in listViatura:
                despacho = Despacho(idOcorrencia, row, current_user.id, datInicio)
                despachoHistorico = DespachoHistorico(despacho, statusDespachoEnum.StatusDespachoEnum.AGUARDANDO_ATENDIMENTO.value, current_user.id, datInicio)
                db.session.add(despachoHistorico)

            ocorrenciaHistorico = db.session.query(OcorrenciaHistorico).join(Ocorrencia).filter(and_(Ocorrencia.id==idOcorrencia, OcorrenciaHistorico.dataFim.is_(None))).first()
            ocorrenciaHistorico.dataFim = datInicio
          
            newOcorrenciaHistorico = OcorrenciaHistorico(ocorrenciaHistorico.ocorrencia, statusOcorrenciaEnum.StatusOcorrenciaEnum.EM_ANDAMENTO.value, current_user.id, datInicio)
            
            db.session.add(newOcorrenciaHistorico)
            db.session.commit()

        except Exception as e:
            db.session.rollback();
            flash('Erro: {}'.format(e), 'error') 
            return render_template('despacho.html', form=form)

        return redirect(url_for('ocorrencia.prepareSearchOcorrencia'))
    
    @despacho_bp.route('/atenderDespacho/<idDespachoHistorico>', methods=['GET'])
    @login_required
    @roles_required('URBANCAD_ADMIN', 'URBANCAD_GOVERNO', 'URBANCAD_DESPACHO')    
    def atenderDespacho(idDespachoHistorico):

        try:
            datInicio = datetime.datetime.now()

            despachoHistorico = db.session.query(DespachoHistorico).filter(and_(DespachoHistorico.id==idDespachoHistorico, DespachoHistorico.dataFim.is_(None))).first()
            despachoHistorico.dataFim = datInicio
          
            newDespachoHistorico = DespachoHistorico(despachoHistorico.despacho, statusDespachoEnum.StatusDespachoEnum.EM_ANDAMENTO.value, current_user.id, datInicio)
            
            db.session.add(newDespachoHistorico)
            db.session.commit()

            flash('Despacho atendido com sucesso', 'sucess')
            redirect(url_for('despacho.meusDespachos'))
        except Exception as e:
            db.session.rollback();
            flash('Erro: {}'.format(e), 'error') 
            redirect(url_for('despacho.meusDespachos')) 
        

    @despacho_bp.route('/meusDespachos', methods=['GET'])
    @login_required
    @roles_required('URBANCAD_ADMIN', 'URBANCAD_GOVERNO', 'URBANCAD_DESPACHO')
    def meusDespachos():
        page = request.args.get('page', 1, type=int)
        listDespachoHistorico = DespachoHistorico.query.filter(and_(DespachoHistorico.idUsuario==current_user.id, DespachoHistorico.dataFim.is_(None))).order_by(DespachoHistorico.dataInicio.desc()).paginate(page=page, per_page=ROWS_PER_PAGE)
        return render_template('meusDespachos.html', listDespachoHistorico=listDespachoHistorico)