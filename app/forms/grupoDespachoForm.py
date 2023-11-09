from wtforms import Form, HiddenField,  SelectField, SubmitField
from wtforms.validators import DataRequired, InputRequired

class GrupoDespachoForm(Form):

    grupoDespacho = SelectField(
        'Grupo de Despacho',
        coerce=int,
        validators = [
            DataRequired(message='*Campo Requerido'),
            InputRequired(message=('*Campo Requerido'))
    ])

    idOcorrencia = HiddenField('Ocorrencia')

    submit = SubmitField('Atribuir')