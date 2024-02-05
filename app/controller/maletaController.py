from base64 import b64encode
import datetime
from flask_login import login_required

from app.controller.roleRequired import roles_required
from ..models.deteccaoVeicular import DeteccaoVeicular
from ..forms.deteccaoSearchForm import DeteccaoSearchForm
from ..rotas.maletaRout import maleta_bp
from flask import redirect, render_template, request, flash, url_for

class viaturaController:    

    global ROWS_PER_PAGE 
    ROWS_PER_PAGE = 20

    @maleta_bp.route('/listarDeteccao', methods=['GET'])
    @login_required
    def listarDeteccao():
        try:
            page = request.args.get('page', 1, type=int)
            form  = DeteccaoSearchForm(request.form)
            listDeteccao = DeteccaoVeicular.query.order_by(DeteccaoVeicular.gps_data_timestamp.desc()).paginate(page=page, per_page=ROWS_PER_PAGE)    

            for row in listDeteccao.items:
                row.fileBase64 = b64encode(row.image).decode()

        except Exception as e:
            flash('Erro: {}'.format(e), 'error')

        return render_template('listarDeteccao.html', listDeteccao=listDeteccao, form=form)
    
    @roles_required('MACEIO_ADMIN', 'CAD_DESPACHO')
    @maleta_bp.route('/searchDeteccao', methods=['GET'])
    @login_required
    def searchDeteccao():

        form = DeteccaoSearchForm(request.form)
        isPlacaSearch = request.args.get('isPlacaSearch')
        form.isPlacaSearch.data = isPlacaSearch
        dataInicioSearch = request.args.get('dataInicioSearch')
        dataFimSearch = request.args.get('dataFimSearch')
        horaInicioSearch = request.args.get('horaInicioSearch')
        horaFimSearch = request.args.get('horaFimSearch')

        page = request.args.get('page', 1, type=int)

        if dataInicioSearch:
            if horaInicioSearch:
                dataInicioSearch = datetime.datetime.strptime(dataInicioSearch + " " + horaInicioSearch,"%Y-%m-%d %H:%M")
                form.horaInicioSearch.data = datetime.datetime.strptime(horaInicioSearch, "%H:%M")
            else:
                dataInicioSearch = datetime.datetime.strptime(dataInicioSearch, '%Y-%m-%d')
            form.dataInicioSearch.data = dataInicioSearch
        if dataFimSearch:
            if horaFimSearch:
                dataFimSearch = datetime.datetime.strptime(dataFimSearch + " " + horaFimSearch, '%Y-%m-%d %H:%M')
                form.horaFimSearch.data = datetime.datetime.strptime(horaFimSearch, "%H:%M")
            else:
                dataFimSearch = datetime.datetime.strptime(dataFimSearch, '%Y-%m-%d')
                dataFimSearch = dataFimSearch.replace(hour=23, minute=59, second=59)
            form.dataFimSearch.data = dataFimSearch

        try: 

            if isPlacaSearch or dataInicioSearch or dataFimSearch:          

                querySearch = DeteccaoVeicular.query

                if isPlacaSearch:
                    querySearch= querySearch.filter(DeteccaoVeicular.plate != None)

                if dataInicioSearch and dataFimSearch:
                    querySearch = querySearch.filter(DeteccaoVeicular.gps_data_timestamp >= dataInicioSearch).filter(DeteccaoVeicular.gps_data_timestamp <= dataFimSearch)
                elif dataInicioSearch and not dataFimSearch:
                    querySearch = querySearch.filter(DeteccaoVeicular.gps_data_timestamp >= dataInicioSearch)
                elif not dataInicioSearch and dataFimSearch:
                    querySearch = querySearch.filter(DeteccaoVeicular.gps_data_timestamp <= dataFimSearch)

                listDeteccao = querySearch.order_by(DeteccaoVeicular.gps_data_timestamp.desc()).paginate(page=page, per_page=ROWS_PER_PAGE)
                for row in listDeteccao.items:
                    row.fileBase64 = b64encode(row.image).decode()
            else:
                return redirect(url_for('maleta.listarDeteccao'))
   
        except Exception as e:
            flash('Erro: {}'.format(e), 'error')

        return render_template('listarDeteccao.html', listDeteccao=listDeteccao, form=form)    