from wtforms.widgets import TextArea
from wtforms import Form, StringField, SelectField, FileField
from wtforms.validators import DataRequired, InputRequired, Length

class ViaturaForm(Form):

    codigo = StringField(
        'Código:',
        render_kw={"placeholder": "Código da viatura."},
        validators = [
            InputRequired(message=('*Campo Requerido')),
            Length(max=30, message='O código deve ter no mínimo %(max)d caracteres')
        ])

    placa = StringField(
        'Placa:',
        render_kw={"placeholder": "Placa da viatura."},
        validators = [
            InputRequired(message=('*Campo Requerido')),
            Length(max=7, message='A placa deve ter no mínimo %(max)d caracteres')
        ])   

    descricao = StringField(
        'Descrição:',
        render_kw={"placeholder": "Descrição da viatura."},
        validators = [
            InputRequired(message=('*Campo Requerido')),
            Length(max=100, message='O código deve ter no mínimo %(max)d caracteres')
        ])        

    instituicao = SelectField(
        'Inistituição',
        coerce=int,
        validators = [
            DataRequired(message='*Campo Requerido'),
            InputRequired(message=('*Campo Requerido'))
    ])

    tipoPatrulha = SelectField(
        'Tipo Patrulha',
        coerce=int,
        validators = [
            DataRequired(message='*Campo Requerido'),
            InputRequired(message=('*Campo Requerido'))
    ])