from wtforms.widgets import TextArea
from ..util.validaCpfUtil import ValidaCpf
from wtforms import Form, StringField, SelectField
from wtforms.validators import DataRequired, InputRequired, Length

class OcorrenciaForm(Form):

    problema = StringField(
        'Qual o problema?',
        widget=TextArea(),
        render_kw={"placeholder": "Faça uma breve descrição do seu problema"},
        validators = [
            InputRequired(message=('*Campo Requerido')),
            Length(max=1000, message='A senha deve ter no mínimo %(max)d caracteres')
        ])

    endereco = StringField(
        'Qual o endereço da ocorrência:',
        render_kw={"placeholder": "Endereço da ocorrência"},
        validators = [
            InputRequired(message=('*Campo Requerido')),
            Length(max=200, message='A senha deve ter no mínimo %(max)d caracteres')
        ])

    latitude = StringField(
        'Lat:',
        render_kw={'readonly': True})

    longitude = StringField(
        'Long:',
        render_kw={'readonly': True})     

    tipoOcorrencia = SelectField(
        'Tipo de Ocorrência',
        coerce=int,
        validators = [
            DataRequired(message='*Campo Requerido'),
            InputRequired(message=('*Campo Requerido'))
    ])

    subtipoOcorrencia = SelectField(
        'Subtipo de Ocorrência',
        coerce=int,
        validators = [
            DataRequired(message='*Campo Requerido'),
            InputRequired(message=('*Campo Requerido'))
    ])

    # Dados do interessdo

    txtInteressado = StringField(
        'Interessado',
        render_kw={"placeholder": "Nome do Interessado"},
        validators = [
            InputRequired(message=('*Campo Requerido')),
            Length(max=1000, message='A senha deve ter no mínimo %(max)d caracteres')
        ])
    
   
    txtCpf = StringField(
        'CPF do Interessado',
        render_kw={'placeholder': 'Digite apenas números', 'class': 'form-control'}, 
        validators = [
            Length(max=11, min=11, message='O CPF deve ter conter exatamente 11 caracteres'),
            ValidaCpf()
    ])

    txtTelefone = StringField(
        'Telefone do Interessado',
        render_kw={'placeholder': 'DDD + Telefone. Digite apenas números', 'class': 'form-control'}, 
        validators = [
            DataRequired(message='*Campo Requerido'),
            Length(max=11, min=11, message='O Telefone deve ter conter exatamente 11 caracteres'),
    ])      