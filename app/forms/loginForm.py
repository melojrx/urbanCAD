from wtforms import Form, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
 
class LoginForm(Form):
    email = StringField(
        'E-mail',
    validators= [
        Email(message=('Ops. Não nos parece um e-mail válido.'))
    ])

    password = PasswordField('Senha', 
    validators = [
        DataRequired(),
        Length(min=8, message='A senha deve ter no mínimo %(min)d caracteres')
    ])

    submit = SubmitField('Entrar')