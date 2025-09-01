from ..database import db
from validate_docbr import CPF
from ..models.userModel import User
from ..forms.loginForm import LoginForm
from ..forms.registerForm import RegisterForm
from ..rotas.loginRout import login_bp
from flask_login import login_user, logout_user
from flask import render_template, request, redirect, url_for, flash, session

class loginController:

    @login_bp.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegisterForm(request.form)

        if request.method == 'POST' and form.validate(): 
            name = form.name.data
            email = form.email.data
            txtcpf = form.cpf.data
            pwd = form.password.data

            cpf = CPF()
            if not cpf.validate(txtcpf): 
               flash('Ops. Não nos parece um CPF válido', 'error')
               return render_template('register.html', form=form)

            if email:
                email = email.lower()

            # Verificar se usuário já existe
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('Este email já está cadastrado.', 'error')
                return render_template('register.html', form=form)

            existing_cpf = User.query.filter_by(cpf=txtcpf).first()
            if existing_cpf:
                flash('Este CPF já está cadastrado.', 'error')
                return render_template('register.html', form=form)

            try:
                # Usar role do formulário ou determinar baseado no email
                role = form.role.data if hasattr(form, 'role') and form.role.data else 'CAD_AGENTE'
                if not role and "admin" in email:
                    role = 'CAD_ADMIN'
                elif not role and ("despacho" in email or "gd" in email):
                    role = 'CAD_DESPACHO'
                elif not role:
                    role = 'CAD_AGENTE'
                
                user = User(name, email, txtcpf, pwd, role)
                db.session.add(user)
                db.session.commit()
                
                flash('Usuário cadastrado com sucesso!', 'success')
                return redirect(url_for('login.login'))
                
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao cadastrar usuário: {e}', 'error')
                
        return render_template('register.html', form=form)   

    @login_bp.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm(request.form)
        
        if request.method == 'POST' and form.validate(): 
            email = form.email.data.lower()
            password = form.password.data
            
            # Busca usuário pelo email
            user = User.query.filter_by(email=email).first()
            
            if user and user.verify_password(password):
                login_user(user)
                
                # Define role na sessão
                session["roles"] = user.role
                
                # Redireciona baseado no role
                if user.role == 'CAD_ADMIN':
                    return redirect(url_for('ocorrencia.iniciar'))
                elif user.role == 'CAD_DESPACHO':
                    return redirect(url_for('despacho.telaDespacho'))
                elif user.role == 'CAD_AGENTE':
                    return redirect(url_for('despacho.meusDespachos'))
                else:
                    # Role não reconhecido
                    flash('Usuário com papel não reconhecido. Entre em contato com o Administrador.', 'error')
                    logout_user()
                    return render_template('login.html', form=form)
            else:
                flash('Email ou senha inválidos.', 'error')
                return render_template('login.html', form=form)
        
        return render_template('login.html', form=form)
            
    @login_bp.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('login.login'))

    @login_bp.route('/site')
    def site():
        logout_user()
        return redirect('/')