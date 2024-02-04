import datetime
from app.forms.despachoObservacaoForm import DespachoObservacaoForm
from app.models.agenteModel import Agente

from app.models.composicaoViaturaModel import ComposicaoViatura
from app.models.despachoObservacaoModel import DespachoObservacao
from app.models.interessadoModel import Interessado
from ..database import db
from sqlalchemy import and_, text
from flask import flash, redirect, render_template, request, session, url_for
from flask_login import login_required, current_user
from ..enum import statusOcorrenciaEnum
from ..enum import statusDespachoEnum
from app.forms.despachoForm import DespachoForm
from app.models.despachoModel import Despacho
from app.models.grupoDespachoModel import GrupoDespacho
from app.models.userModel import User
from app.models.usuarioGrupoDespachoModel import UsuarioGrupoDespacho
from app.models.ocorrenciaHistoricoModel import OcorrenciaHistorico
from app.models.ocorrenciaGrupoDespachoModel import OcorrenciaGrupoDespacho
from app.models.subtipoOcorrenciaModel import SubtipoOcorrencia
from app.models.ocorrenciaModel import Ocorrencia
from app.models.despachoHistoricoModel import DespachoHistorico
from .roleRequired import roles_required
from ..rotas.despachoRout import despacho_bp
from sqlalchemy.orm import joinedload
from app import socketio

class DespachoController():
      
    global ROWS_PER_PAGE 
    ROWS_PER_PAGE = 10
    
    @classmethod
    def getListDespacho(cls):

        querySearchDespacho = None
        querySearchADespachar = None

        if not 'URBANCAD_ADMIN' in session["roles"]:  
              
            querySearchDespacho = (Ocorrencia.query
                        .join(Interessado)
                        .join(Despacho)
                        .join(SubtipoOcorrencia, 'subtipoOcorrencia')
                        .join(ComposicaoViatura)
                        .join(OcorrenciaHistorico)
                        .join(OcorrenciaGrupoDespacho)
                        .join(GrupoDespacho)
                        .join(UsuarioGrupoDespacho)
                        .join(User)
                        .options(
                            joinedload('interessado')
                            ,joinedload('listDespacho')
                            ,joinedload('subtipoOcorrencia').joinedload('tipoOcorrencia')
                        )
                        .filter(
                            OcorrenciaHistorico.idStatusOcorrencia == statusOcorrenciaEnum.StatusOcorrenciaEnum.EM_ANDAMENTO.value, 
                            User.id == current_user.id,
                            OcorrenciaHistorico.dataFim.is_(None))
                        )

            querySearchADespachar = (OcorrenciaHistorico.query
                .join(Ocorrencia)
                .join(Interessado)
                .join(SubtipoOcorrencia, Ocorrencia.subtipoOcorrencia)
                .outerjoin(Despacho, Despacho.idOcorrencia == Ocorrencia.id)
                .join(OcorrenciaGrupoDespacho)
                .join(GrupoDespacho)
                .join(UsuarioGrupoDespacho)
                .options(
                            joinedload('ocorrencia').joinedload('interessado')
                            ,joinedload('ocorrencia.subtipoOcorrencia').joinedload('tipoOcorrencia')
                        )
                .filter(
                    OcorrenciaHistorico.dataFim.is_(None),
                    Despacho.id.is_(None),
                    UsuarioGrupoDespacho.idUsuario == current_user.id
                )
            )
        else:
            querySearchDespacho = (Ocorrencia.query
                        .join(Interessado)
                        .join(Despacho)
                        .join(SubtipoOcorrencia, 'subtipoOcorrencia')
                        .join(ComposicaoViatura)
                        .join(OcorrenciaHistorico)
                        .options(
                            joinedload('interessado')
                            ,joinedload('listDespacho')
                            ,joinedload('subtipoOcorrencia').joinedload('tipoOcorrencia')
                        )
                        .filter(
                            OcorrenciaHistorico.idStatusOcorrencia == statusOcorrenciaEnum.StatusOcorrenciaEnum.EM_ANDAMENTO.value, 
                            OcorrenciaHistorico.dataFim.is_(None))
                        )

            querySearchADespachar = (OcorrenciaHistorico.query
                .join(Ocorrencia)
                .join(Interessado)
                .join(SubtipoOcorrencia, Ocorrencia.subtipoOcorrencia)
                .outerjoin(Despacho, Despacho.idOcorrencia == Ocorrencia.id)
                .options(
                            joinedload('ocorrencia').joinedload('interessado')
                            ,joinedload('ocorrencia.subtipoOcorrencia').joinedload('tipoOcorrencia')
                        )
                .filter(
                    OcorrenciaHistorico.dataFim.is_(None),
                    Despacho.id.is_(None)
                    )
            )          

        listOcorrenciaDespachada = querySearchDespacho.order_by(OcorrenciaHistorico.dataInicio.desc()).all()

        # O código abaixo habilita o botão de finalizar Ocorrência caso todos os despachos estejam Concluídos      
        for ocorrencia in listOcorrenciaDespachada:
                if all(row.despachoHistorico.idStatusDespacho == statusDespachoEnum.StatusDespachoEnum.CONCLUIDO.value for row in ocorrencia.listDespacho):
                    ocorrencia.exibeFinalizarOcorrencia = True

        listDespachar = querySearchADespachar.order_by(OcorrenciaHistorico.dataInicio.desc()).all()



        return  listOcorrenciaDespachada, listDespachar

    @classmethod
    def getIdRegiaoByUser(cls):
        sqlRegional = text("SELECT id"  
                    " FROM cad.tb_regionais_reg reg"
                    " JOIN cad.tb_grupo_despacho_gde gde ON reg.id = gde.id_regional_gde"
                    " JOIN cad.tb_usuario_grupo_despacho_ugd ugd ON gde.id_grupo_despacho_gde = ugd.id_grupo_despacho_ugd "
                    " WHERE ugd.id_usuario_ugd = :param;")
        resultRegional = db.engine.execute(sqlRegional, param=current_user.id)
        row = resultRegional.fetchone()

        return row["id"]

    @despacho_bp.route('/telaDespacho', methods=['GET'])
    @login_required
    @roles_required('URBANCAD_ADMIN', 'URBANCAD_DESPACHO')    
    def telaDespacho():
        form = DespachoForm(request.form)

        form.idRegiao.data = DespachoController.getIdRegiaoByUser();

        listOcorrenciaDespachada, listDespachar = DespachoController.getListDespacho()
        return render_template('despacho.html', form=form, listOcorrenciaDespachada=listOcorrenciaDespachada, listDespachar=listDespachar)

    @despacho_bp.route('/prepareDespachar/<idOcorrencia>', methods=['GET'])
    @login_required
    @roles_required('URBANCAD_ADMIN', 'URBANCAD_GOVERNO', 'URBANCAD_DESPACHO')    
    def prepareDespachar(idOcorrencia):

        form = DespachoForm(request.form)
        form.ocorrencia.data = idOcorrencia

        ocorrencia = Ocorrencia.query.filter(Ocorrencia.id == idOcorrencia).first()
        
        sql = text("SELECT cvi.id_composicao_viatura_cvi, via.txt_codigo_via, via.txt_placa_via, tpa.txt_tipo_patrulha_tpa, ins.txt_instituicao_ins"  
                    " FROM cad.tb_viatura_via via"
                    " JOIN cad.tb_tipo_patrulha_tpa tpa ON via.id_tipo_patrulha_via = tpa.id_tipo_patrulha_tpa"
                    " JOIN cad.tb_instituicao_ins ins ON via.id_instituicao_via = ins.id_instituicao_ins"
                    " JOIN cad.tb_composicao_viatura_cvi cvi ON via.id_viatura_via = cvi.id_viatura_cvi"
                    # " JOIN cad.tb_composicao_com com ON cvi.id_composicao_viatura_cvi = com.id_composicao_viatura_com"
                    " JOIN cad.tb_agente_age a ON cvi.id_agente_cvi = a.id_agente_age"
                    " JOIN comum.tb_usuario_usu usu ON a.id_usuario_age = usu.id_usuario_usu"
                    " JOIN cad.tb_usuario_grupo_despacho_ugd ugd ON usu.id_usuario_usu = ugd.id_usuario_ugd"
                    " JOIN cad.tb_grupo_despacho_gde gde ON ugd.id_grupo_despacho_ugd = gde.id_grupo_despacho_gde"
                    " JOIN cad.tb_regionais_reg reg ON gde.id_regional_gde = reg.id"
                    " WHERE"
                    " cvi.dat_fim_cvi is null AND"
                    " a.dat_fim_age is null AND"
                    " ugd.dat_fim_ugd is null AND"
                    " gde.dat_fim_gde is null AND"
                    " ST_Contains(geom, ST_SetSRID(ST_MakePoint(:param1, :param2), 4326));")
        result = db.engine.execute(sql, param1=ocorrencia.txtLong, param2=ocorrencia.txtLat)

        if(not result.rowcount):
            flash('Nenhuma viatura disponível para a região', 'error')
            return

        form.despacharPara.choices = [(row["id_composicao_viatura_cvi"], 
                                       str(row["txt_tipo_patrulha_tpa"]) + " " + 
                                       str(row["txt_instituicao_ins"]) + " " + 
                                       str(row["txt_codigo_via"]) + " " + 
                                       str(row["txt_placa_via"])) for row in result]
                   
        return render_template('formDespacho.html', form=form, ocorrencia=ocorrencia)

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

            socketio.emit('atualizar_lista_ocorrencia')
            flash('Despacho Realizado com sucesso', 'sucess')
            return redirect(url_for('despacho.telaDespacho'))
        except Exception as e:
            db.session.rollback();
            flash('Erro: {}'.format(e), 'error') 
            return render_template('despacho.html', form=form)
   
    @despacho_bp.route('/atenderDespacho/<idDespachoHistorico>', methods=['GET'])
    @login_required
    @roles_required('URBANCAD_ADMIN', 'URBANCAD_AGENTE', 'URBANCAD_DESPACHO')    
    def atenderDespacho(idDespachoHistorico):

        try:
            datInicio = datetime.datetime.now()

            despachoHistorico = db.session.query(DespachoHistorico).filter(and_(DespachoHistorico.id==idDespachoHistorico, DespachoHistorico.dataFim.is_(None))).first()
            despachoHistorico.dataFim = datInicio
          
            newDespachoHistorico = DespachoHistorico(despachoHistorico.despacho, statusDespachoEnum.StatusDespachoEnum.EM_ANDAMENTO.value, current_user.id, datInicio)
            
            db.session.add(newDespachoHistorico)
            db.session.commit()

            flash('Despacho atendido com sucesso', 'sucess')
            return redirect(url_for('despacho.meusDespachos'))
        except Exception as e:
            db.session.rollback();
            flash('Erro: {}'.format(e), 'error') 
            return redirect(url_for('despacho.meusDespachos')) 
        
    @despacho_bp.route('/gerenciarDespacho/<idDespachoHistorico>', methods=['GET'])
    @login_required
    @roles_required('URBANCAD_ADMIN', 'URBANCAD_AGENTE', 'URBANCAD_DESPACHO')    
    def gerenciarDespacho(idDespachoHistorico):

        try:
            form = DespachoObservacaoForm(request.form)
            despachoHistorico = db.session.query(DespachoHistorico).filter(DespachoHistorico.id==idDespachoHistorico).first()
            form.idDespachoHistorico.data = despachoHistorico.id
                                          
            return render_template('gerenciarDespacho.html', form=form, despachoHistorico=despachoHistorico)
        except Exception as e:
            db.session.rollback()
            flash('Erro: {}'.format(e), 'error') 
            return redirect(url_for('despacho.meusDespachos')) 

    @despacho_bp.route('/cadastrarObservacao', methods=['POST'])
    @login_required
    @roles_required('URBANCAD_ADMIN', 'URBANCAD_AGENTE', 'URBANCAD_DESPACHO')    
    def cadastrarObservacao():

        try:
            form = DespachoObservacaoForm(request.form)
            file = request.files['file']
            datInicio = datetime.datetime.now()
            despachoObservacao = DespachoObservacao(form.idDespachoHistorico.data, current_user.id, form.observacao.data, file.read(), datInicio)

            db.session.add(despachoObservacao)
            db.session.commit()

            return redirect(url_for('despacho.gerenciarDespacho', idDespachoHistorico=form.idDespachoHistorico.data))
        except Exception as e:
            db.session.rollback()
            flash('Erro: {}'.format(e), 'error') 
            return redirect(url_for('despacho.gerenciarDespacho', idDespachoHistorico=form.idDespachoHistorico.data))    

    @despacho_bp.route('/meusDespachos', methods=['GET'])
    @login_required
    @roles_required('URBANCAD_ADMIN', 'URBANCAD_AGENTE', 'URBANCAD_DESPACHO')
    def meusDespachos():
        page = request.args.get('page', 1, type=int)
        listDespachoHistorico = DespachoHistorico.query.join(Despacho).join(ComposicaoViatura).join(Agente).filter(and_(Agente.idUsuario==current_user.id, DespachoHistorico.dataFim.is_(None))).order_by(DespachoHistorico.dataInicio.desc()).paginate(page=page, per_page=ROWS_PER_PAGE)
        return render_template('meusDespachos.html', listDespachoHistorico=listDespachoHistorico)
    
    @despacho_bp.route('/finalizarDespacho/<idDespachoHistorico>', methods=['GET'])
    @login_required
    @roles_required('URBANCAD_ADMIN', 'URBANCAD_AGENTE')    
    def finalizarDespacho(idDespachoHistorico):
        try:

            datInicio = datetime.datetime.now()

            despachoHistorico = db.session.query(DespachoHistorico).filter(and_(DespachoHistorico.id==idDespachoHistorico, DespachoHistorico.dataFim.is_(None))).first()
            despachoHistorico.dataFim = datInicio
          
            newDespachoHistorico = DespachoHistorico(despachoHistorico.despacho, statusDespachoEnum.StatusDespachoEnum.CONCLUIDO.value, current_user.id, datInicio)
            
            db.session.add(newDespachoHistorico)
            db.session.commit()

            flash('Despacho finalizado com sucesso', 'sucess')
            return redirect(url_for('despacho.meusDespachos'))
        except Exception as e:
            db.session.rollback()
            flash('Erro: {}'.format(e), 'error') 
            return redirect(url_for('despacho.meusDespachos'))
        
    @despacho_bp.route("/loadListADespachar",methods=["POST","GET"])
    @login_required
    def loadListADespachar():
        form = DespachoForm(request.form)
        form.idRegiao.data = DespachoController.getIdRegiaoByUser();
        listOcorrenciaDespachada, listDespachar = DespachoController.getListDespacho()
        return render_template('loadListaDespacho.html', form=form, listOcorrenciaDespachada=listOcorrenciaDespachada, listDespachar=listDespachar)