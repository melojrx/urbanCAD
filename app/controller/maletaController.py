from flask_login import login_required
from ..models.deteccaoVeicular import DeteccaoVeicular
from ..rotas.maletaRout import maleta_bp
from flask import render_template, request, flash

class viaturaController:    

    global ROWS_PER_PAGE 
    ROWS_PER_PAGE = 20

    @maleta_bp.route('/listarDeteccao', methods=['GET'])
    @login_required
    def listarDeteccao():
        try:
            page = request.args.get('page', 1, type=int)
            
            listDeteccao = DeteccaoVeicular.query.order_by(DeteccaoVeicular.gps_data_timestamp.desc()).paginate(page=page, per_page=ROWS_PER_PAGE)    

        except Exception as e:
            flash('Erro: {}'.format(e), 'error')

        return render_template('listarDeteccao.html', listDeteccao=listDeteccao)