from wtforms.widgets import TextArea
from ..util.validaCpfUtil import ValidaCpf
from wtforms import Form, StringField, SelectField, BooleanField
from wtforms.validators import DataRequired, InputRequired, Length

class OcorrenciaForm(Form):

    problema = StringField(
        'Descreva a ocorrência:',
        widget=TextArea(),
        render_kw={"placeholder": "Faça uma breve descrição do seu problema"},
        validators = [
            InputRequired(message=('*Campo Requerido')),
            Length(max=1000, message='A senha deve ter no mínimo %(max)d caracteres')
        ])

    endereco = StringField(
        'Endereço da ocorrência:',
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
        'Tipo de Ocorrência:',
        coerce=int,
    #     validators = [
    #         DataRequired(message='*Campo Requerido'),
    #         InputRequired(message=('*Campo Requerido'))
    # ]
    )

    subtipoOcorrencia = SelectField(
        'Subtipo de Ocorrência:',
        coerce=int,
    #     validators = [
    #         DataRequired(message='*Campo Requerido'),
    #         InputRequired(message=('*Campo Requerido'))
    # ]
    )

    # Dados do interessdo

    txtInteressado = StringField(
        'Noticiante:',
        render_kw={"placeholder": "Nome do Noticiante"},
        validators = [
            InputRequired(message=('*Campo Requerido')),
            Length(max=1000, message='A senha deve ter no mínimo %(max)d caracteres')
        ])
    
   
    txtCpf = StringField(
        'CPF do Noticiante:',
        render_kw={'placeholder': 'CPF', 'class': 'form-control'}, 
        validators = [
            Length(max=11, min=11, message='O CPF deve ter conter exatamente 11 caracteres'),
            ValidaCpf()
    ])

    txtRg = StringField(
        'RG do Noticiante:',
        render_kw={'placeholder': 'RG', 'class': 'form-control'}, 
    )

    txtPassaporte = StringField(
        'Passaporte do Noticiante:',
        render_kw={'placeholder': 'Passaporte', 'class': 'form-control'}, 
    )

    txtTelefone = StringField(
        'Telefone do Noticiante:',
        render_kw={'placeholder': 'DDD + Telefone. Digite apenas números', 'class': 'form-control'}, 
    #     validators = [
    #         DataRequired(message='*Campo Requerido'),
    #         Length(max=11, min=11, message='O Telefone deve ter conter exatamente 11 caracteres'),
    # ]
    )

    isNoticianteVitima = BooleanField(
        'Noticiante é a vítima?'
    )

    isNoticianteEstrangeiro = BooleanField(
        'Noticiante é estrangeiro?'
    )