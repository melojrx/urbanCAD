
from app.DTO.ocorrenciaDTO import OcorrenciaDTO
from app.DAO.ocorrenciaDao import OcorrenciaDao
from ..rotas.dashboardRout import dashboard_bp
from .roleRequired import roles_required
from flask_login import login_required
from flask import flash, render_template

class dashboardController():

    @dashboard_bp.route('/dashboard')
    @login_required
    @roles_required('CAD_ADMIN', 'CAD_DESPACHO')
    def dashboard():
        try:

            # Resultado do gráfico pizza de ocorrência por status
            resultByStatus = OcorrenciaDao.getOcorrenciaByStatus()
            listOcorrenciaByStatus = []
            ocorrencia = None
            for row in resultByStatus:
                ocorrencia = OcorrenciaDTO(row['data'], row['label'])
                listOcorrenciaByStatus.append(ocorrencia)
            listOcorrenciaByStatus = [ocorrencia.to_dict() for ocorrencia in listOcorrenciaByStatus]

            # Resultado do gráfico barra de ocorrência por região
            resultByRegiao = OcorrenciaDao.getOcorrenciaByRegiao()
            listOcorrenciaByRegiao = []
            ocorrencia = None
            for row in resultByRegiao:
                ocorrencia = OcorrenciaDTO(row['data'], row['label'])
                listOcorrenciaByRegiao.append(ocorrencia)
            listOcorrenciaByRegiao = [ocorrencia.to_dict() for ocorrencia in listOcorrenciaByRegiao]

            ocorrenciaTotais = OcorrenciaDao.getCountOcorrenciaTotal()
            ocorrenciaEmAndamento = OcorrenciaDao.getCountOcorrenciaEmAndamento()
            ocorrenciaFinalizada = OcorrenciaDao.getCountOcorrenciaFinalizada()
            ocorrenciaDespachada = OcorrenciaDao.getCountOcorrenciaDespachada()


            listOcorrencia = OcorrenciaDao.getListOcorrenciaFinalizada(1)

        except Exception as e:
            flash('Erro: {}'.format(e), 'error')
        return render_template('dashboard.html', listOcorrenciaByStatus=listOcorrenciaByStatus, 
                                    listOcorrenciaByRegiao=listOcorrenciaByRegiao, 
                                    ocorrenciaTotais=ocorrenciaTotais,
                                    ocorrenciaEmAndamento=ocorrenciaEmAndamento,
                                    ocorrenciaFinalizada=ocorrenciaFinalizada,
                                    ocorrenciaDespachada=ocorrenciaDespachada,
                                    listOcorrencia=listOcorrencia
                                )
