from ..util.validaCpfUtil import ValidaCpf
from wtforms import Form, HiddenField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, InputRequired, Length

class UsuarioForm(Form):

    id = HiddenField('id')

    name = StringField(
    'Nome',
    [
        InputRequired(message=('Por favor, informe seu Nome.'))
    ])

    email = StringField(
    'E-mail',
    validators = [
        Email(message=('Ops. Não nos parece um e-mail válido.'))
    ])

    cpf = StringField(
    'CPF',
    render_kw={'placeholder': 'Digite apenas números', 'class': 'form-control'}, 
    validators = [
        DataRequired(message='*Campo Requerido'),
        Length(max=11, min=11, message='O CPF deve ter conter exatamente 11 caracteres'),
        ValidaCpf()
    ])

    submit = SubmitField('Alterar')