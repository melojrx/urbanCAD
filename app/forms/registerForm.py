from ..util.validaCpfUtil import ValidaCpf
from wtforms import BooleanField, Form, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired, Length

class RegisterForm(Form):

    name = StringField(
    'Digite seu Nome',
    [
        InputRequired(message=('Por favor, informe seu Nome.'))
    ])

    email = StringField(
    'Digite seu email',
    validators = [
        Email(message=('Ops. Não nos parece um e-mail válido.'))
    ])

    cpf = StringField(
    'Digite seu CPF',
    render_kw={'placeholder': 'Digite apenas números', 'class': 'form-control'}, 
    validators = [
        DataRequired(message='*Campo Requerido'),
        Length(max=11, min=11, message='O CPF deve ter conter exatamente 11 caracteres'),
        ValidaCpf()
    ])

    password = PasswordField('Digite sua Senha', 
    validators = [
        DataRequired(),
        EqualTo('confirm_password', message='As senhas não são iguais'),
        Length(min=8, message='A senha deve ter no mínimo %(min)d caracteres')
    ])

    confirm_password = PasswordField('Confirme sua senha',
    validators = [
        DataRequired(message='*Campo Requerido'),
        EqualTo('password', message='As senhas devem ser iguais')
    ])

    accept_tos = BooleanField('Você aceita os termos de serviço?', 
    default=True, render_kw ={'checked':''},
    validators = [
        DataRequired(message='*Campo Requerido'),
    ])

    newsletters = BooleanField('Deseja receber as nossas Newsletters?', 
    default=True, render_kw ={'checked':''},
    validators = [
        DataRequired(message='*Campo Requerido'),
    ])   

    submit = SubmitField('Cadastrar')