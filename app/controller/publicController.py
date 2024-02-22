from flask import flash, redirect, render_template, request, url_for
import requests
from app.forms.resetPasswordForm import ResetPasswordForm
from app.rotas.publicRout import public_bp


class publicController:    

    @public_bp.route('/', methods=['GET'])
    def home():
        return render_template('index.html')
    
    @public_bp.route('/esqueciSenha/', methods=['GET'])
    def esqueciSenha():
        form = ResetPasswordForm(request.form)
        return render_template('resetPassword.html', form=form)
    
    @public_bp.route('/enviarEmail/', methods=['POST'])
    def enviarEmail():
        form = ResetPasswordForm(request.form)
        email = form.email.data

        url = 'http://10.82.85.8:8012/api/b2in/auth/password/reset?email=' + form.email.data
        data = {
            'email': email
        }
        headers = {'Content-Type': 'application/json'}

        try:

            response = requests.post(url, json=data, headers=headers)
            response_data = response.json()
            print('response.status_code ', response.status_code)
            print(response_data)

            if(response.status_code == 200):
                flash('E-mail enviado com sucesso','sucess')
            else:
                flash('Um erro ocorreu no envio do E-mail. Tente novamente','error')

        except Exception as e:
            flash('Um erro desconhecido ocorreu no envio do E-mail. Tente novamente', 'error')

        return redirect(url_for('login.login'))     