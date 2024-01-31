from ..database import db
from validate_docbr import CPF
from ..models.userModel import User
from ..forms.loginForm import LoginForm
from ..forms.registerForm import RegisterForm
from ..rotas.loginRout import login_bp
from flask_login import login_user, logout_user
from flask import render_template, request, redirect, url_for, flash, session, jsonify
import requests

class loginController:

    global app_key 
    app_key = '52f3e7a57351afc533bc384ca914a2c8b56a818b0d81d2b38b7934b6'
    global institution_external_id
    institution_external_id = 'cff955b7939ec690e6b63d82ffca69de1a45184b292e9792d8aa709f'

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

            try:
                
                user = User(name, email, txtcpf)
                db.session.add(user)
                
                url = 'http://10.82.85.8:8080/api/b2in/user/role'
                data = {'institution_external_id': institution_external_id, 'email': email, 'password': pwd, "application_external_id": app_key, "role_name": "URBANCAD_USER", 'type': 'USER'}
                headers = {'Content-Type': 'application/json'}
                response = requests.post(url, json=data, headers=headers)
                data = response.json() 
                #print(response.status_code)
                #print(response.json())
                
                if(response.status_code != 201):
                    db.session.rollback()
                    flash('Erro: {}'.format(response.status_code), 'error') 
                    flash('Erro: {}. {}'.format(response.status_code, data['message']), 'error') 
                    return render_template('login.html', form=form)
                else:
                    db.session.commit()
                    flash('Usuário cadastrado com sucesso', 'sucess')
                    return redirect(url_for('login.login')) 
            except Exception as e:
                db.session.rollback()
                flash('Erro: {}'.format(e), 'error')  
        return render_template('register.html', form=form)   

    @login_bp.route('/login', methods=['GET', 'POST'] )
    def login():
        form = LoginForm(request.form)
        if request.method == 'POST' and form.validate(): 
            user = User.query.filter_by(email=form.email.data).first()
            login_user(user)
            if "admin" in user.email:
                session["roles"] = 'URBANCAD_ADMIN'
                return redirect(url_for('ocorrencia.iniciar')) 
            if "gd" in user.email:
                session["roles"] = 'URBANCAD_DESPACHO'
                return redirect(url_for('despacho.telaDespacho')) 
            if "agente" in user.email:
                session["roles"] = 'URBANCAD_AGENTE'
                return redirect(url_for('despacho.meusDespachos'))             
        else:
             return render_template('login.html', form=form)
        # ------------------------------------------------
        form = LoginForm(request.form)

        if request.method == 'POST' and form.validate(): 

            email = form.email.data
            pwd = form.password.data

            try:

                url = 'http://10.82.85.8:8080/api/b2in/auth'
                data = {'email': email, 'password': pwd, 'app_key': app_key, 'type': 'WEB'}
                headers = {'Content-Type': 'application/json'}
                response = requests.post(url, json=data, headers=headers)
                data = response.json()
                #print(response.status_code)

                if(response.status_code == 200):
                    
                    user = User.query.filter(User.email == email).first()
                    #user.roles = data['roles']
                    #print(data['roles'])
 
                    session["roles"] = data['roles']
                    login_user(user)
                    return redirect(url_for('viatura.listarViaturas'))
                elif(response.status_code == 500):
                    flash('Erro: {}. {}'.format(response.status_code, data['Login indisponível']), 'error')                  
                else:
                    flash('Erro: {}. {}'.format(response.status_code, data['message']), 'error') 
                    return render_template('login.html', form=form)
            except Exception as e:
                flash('Erro: {}'.format(e), 'error')             
                return render_template('login.html', form=form)
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