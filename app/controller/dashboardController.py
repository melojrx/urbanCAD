
from app.DTO.ocorrenciaDTO import OcorrenciaDTO
from app.DAO.ocorrenciaDao import OcorrenciaDao
from ..database import db
from ..rotas.dashboardRout import dashboard_bp
from .roleRequired import roles_required
from flask_login import login_required
from flask import flash, redirect, render_template, url_for

class dashboardController():
        
    global ROWS_PER_PAGE 
    ROWS_PER_PAGE = 10

    @dashboard_bp.route('/dashboard')
    @login_required
    @roles_required('MACEIO_ADMIN', 'CAD_DESPACHO')
    def dashboard():
        try:

            result = OcorrenciaDao.getOcorrenciaByDate()

            listOcorrencia = []
            ocorrencia = None
            for row in result:
                ocorrencia = OcorrenciaDTO(row['total'], row['status'])
                listOcorrencia.append(ocorrencia)

        except Exception as e:
            flash('Erro: {}'.format(e), 'error')
        return render_template('dashboard.html', listOcorrencia=listOcorrencia)
