from app.models.ocorrenciaHistoricoModel import OcorrenciaHistorico
from ..rotas.ocorrenciaRout import ocorrencia_bp
from .roleRequired import roles_required
from ..enum import statusOcorrenciaEnum
from flask_login import login_required, current_user
from sqlalchemy import func, and_
from flask import render_template

class ocorrenciaController():
        
    global ROWS_PER_PAGE 
    ROWS_PER_PAGE = 5

    @ocorrencia_bp.route('/homeGoverno', methods=['GET'])
    @login_required
    @roles_required('URBANCAD_ADMIN, URBANCAD_GOVERNO')
    def homeGoverno():
        listOcorrenciaHistorico = OcorrenciaHistorico.query.filter(and_(OcorrenciaHistorico.idStatusOcorrencia != statusOcorrenciaEnum.StatusOcorrenciaEnum.FINALIZADO.value, OcorrenciaHistorico.dataFim.is_(None))).order_by(OcorrenciaHistorico.dataInicio.desc()).limit(10).all()
        return render_template('homeGoverno.html', listOcorrenciaHistorico=listOcorrenciaHistorico)