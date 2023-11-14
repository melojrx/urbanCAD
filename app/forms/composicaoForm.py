from wtforms import Form, SelectField, SubmitField
from wtforms.validators import DataRequired, InputRequired

class ComposicaoForm(Form):  

    agente = SelectField(
        'Agente',
        coerce=int,
        validators = [
            DataRequired(message='*Campo Requerido'),
            InputRequired(message=('*Campo Requerido'))
    ])

    viatura = SelectField(
        'Viatura',
        coerce=int,
        validators = [
            DataRequired(message='*Campo Requerido'),
            InputRequired(message=('*Campo Requerido'))
    ])

    submit = SubmitField('Cadastrar') 