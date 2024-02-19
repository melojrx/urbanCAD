from wtforms import Form, HiddenField, StringField, SubmitField
from wtforms.validators import InputRequired

class TipoPatrulhaForm(Form):

    id = HiddenField('id')

    txtTipoPatrulha = StringField(
        'Tipo de Patrulha:',
        render_kw={"placeholder": "Tipo de Patrulha"},
        validators = [
            InputRequired(message=('*Campo Requerido'))
        ])
    
    submit = SubmitField('Cadastrar')