from wtforms import EmailField, Form, SubmitField
from wtforms.validators import DataRequired, Email

class ResetPasswordForm(Form):  

    email = EmailField (
        'E-mail:',
        render_kw={"placeholder": "Informe seu e-mail."},
        validators = [
            DataRequired(message=('*Campo Requerido')),
            Email()
        ])

    submit = SubmitField('Enviar') 