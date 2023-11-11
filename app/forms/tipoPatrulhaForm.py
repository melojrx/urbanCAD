from wtforms import Form, StringField, SubmitField
from wtforms.validators import InputRequired

class TipoPatrulhaForm(Form):

    descricao = StringField(
        'Tipo de Patrulha:',
        render_kw={"placeholder": "Tipo de Patrulha"},
        validators = [
            InputRequired(message=('*Campo Requerido'))
        ])
    
    submit = SubmitField('Cadastrar')