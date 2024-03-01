from ..database import db
from flask_login import current_user, login_required
from ..models.userModel import User
from ..rotas.usuarioRout import usuario_bp
from ..forms.usuarioForm import UsuarioForm
from flask import redirect, render_template, request, flash, url_for

class usuarioController:    

    @usuario_bp.route('/prepareUpdate', methods=['GET'])
    @login_required
    def prepareUpdate():
        try:
            user = User.query.filter(User.id == current_user.id).first()
            form = UsuarioForm(request.form, obj=user) 
        except Exception as e:
            flash('Erro: {}'.format(e), 'error')

        return render_template('usuario/meusDados.html', form=form)
    
    @usuario_bp.route('/update', methods=['POST'])
    @login_required
    def update():
        try:

            form = UsuarioForm(request.form) 
            user = User(form.name.data, form.email.data, form.cpf.data)
            user.id = form.id.data
            db.session.merge(user)
            db.session.commit()
            
            flash('Dados alterado com sucesso', 'sucess')
        except Exception as e:
            db.session.rollback()
            flash('Erro: {}'.format(e), 'error')

        return redirect(url_for('usuario.prepareUpdate'))    
    
