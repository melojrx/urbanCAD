from wtforms import Form, HiddenField, StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length

class ViaturaForm(Form):

    id = HiddenField('id')

    txtCodigo = StringField(
        'Código:',
        render_kw={"placeholder": "Código da viatura."},
        validators = [
            InputRequired(message=('*Campo Requerido')),
            Length(max=30, message='O código deve ter no mínimo %(max)d caracteres')
        ])

    txtPlaca = StringField(
        'Placa:',
        render_kw={"placeholder": "Placa da viatura."},
        validators = [
            InputRequired(message=('*Campo Requerido')),
            Length(max=7, message='A placa deve ter no mínimo %(max)d caracteres')
        ])   

    txtDescricao = StringField(
        'Descrição:',
        render_kw={"placeholder": "Descrição da viatura."},
        validators = [
            InputRequired(message=('*Campo Requerido')),
            Length(max=100, message='O código deve ter no mínimo %(max)d caracteres')
        ])        

    idInstituicao = SelectField(
        'Instituição:',
        coerce=int,
        validators = [
            DataRequired(message='*Campo Requerido'),
            InputRequired(message=('*Campo Requerido'))
    ])

    idTipoPatrulha = SelectField(
        'Tipo Patrulha:',
        coerce=int,
        validators = [
            DataRequired(message='*Campo Requerido'),
            InputRequired(message=('*Campo Requerido'))
    ])

    submit = SubmitField('Cadastrar')