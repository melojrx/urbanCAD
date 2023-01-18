from ..database import db
from validate_docbr import CPF
from ..models.userModel import User
from ..forms.loginForm import LoginForm
from ..forms.registerForm import RegisterForm
from ..rotas.loginRout import login_bp
from flask_session import Session
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

            user = User.query.filter_by(email=email).first()
            if user:
                flash('Endereço de e-mail já existe', 'exist')
                return redirect(url_for('login.register'))
            else:
                user = User(name, email, txtcpf, pwd)
                db.session.add(user)
                db.session.commit()

                return redirect(url_for('login.login')) 

        return render_template('register.html', form=form)

    @login_bp.route('/login', methods=['GET', 'POST'] )
    def login():

        form = LoginForm(request.form)

        if request.method == 'POST' and form.validate(): 

            email = form.email.data
            pwd = form.password.data

            user = User.query.filter_by(email=email).first()

            if not user or not user.verify_password(pwd):
                flash('Usuário ou senha inválidos')
                return redirect(url_for('login.login'))        

            session["userGoverno"] = user.flgGoverno 
            session["userAdmin"] = user.flgAdmin
            login_user(user)

            if user.flgGoverno:
                return redirect(url_for('evento.homeGoverno'))  
            else:
                return redirect(url_for('evento.home'))  

        else:
            return render_template('login.html', form=form)
            

    @login_bp.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('login.login'))

    @login_bp.route('/site')
    def site():
        logout_user()
        return redirect('/')