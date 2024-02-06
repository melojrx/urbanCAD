


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
        return render_template('dashboard.html')
