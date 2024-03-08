from app.DAO.ocorrenciaDTO import OcorrenciaDTO
from app.DAO.ocorrenciaDao import OcorrenciaDao
from app.controller.roleRequired import roles_required
from ..database import db
from flask_login import login_required
from ..rotas.chartRout import chart_bp
from flask import render_template, request, redirect, url_for, flash

class chartController:    

    @chart_bp.route('/charts', methods=['GET'])
    @login_required
    @roles_required('MACEIO_ADMIN')
    def charts():
        try:

            result = OcorrenciaDao.getOcorrenciaByDate()

            listOcorrencia = []
            ocorrencia = None
            for row in result:
                ocorrencia = OcorrenciaDTO(row['total'], row['status'])
                listOcorrencia.append(ocorrencia) 
                            
        except Exception as e:
            flash('Erro: {}'.format(e), 'error')

        return render_template('charts/charts.html', listOcorrencia=listOcorrencia)   