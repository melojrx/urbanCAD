from wtforms import Form, SelectField, SubmitField
from wtforms.validators import DataRequired, InputRequired

class AgenteForm(Form):  

    usuario = SelectField(
        'Usuário',
        coerce=int,
        validators = [
            DataRequired(message='*Campo Requerido'),
            InputRequired(message=('*Campo Requerido'))
    ])

    instituicao = SelectField(
        'Instituição',
        coerce=int,
        validators = [
            DataRequired(message='*Campo Requerido'),
            InputRequired(message=('*Campo Requerido'))
    ])

    submit = SubmitField('Cadastrar') 