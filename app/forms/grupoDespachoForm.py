from wtforms import Form, HiddenField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, InputRequired

class GrupoDespachoForm(Form):  

    id = HiddenField('id')

    txtNome = StringField(
        'Grupo de Despacho:',
        render_kw={"placeholder": "Nome da Regional"},
        validators = [
            InputRequired(message=('*Campo Requerido'))
        ])

    idRegional = SelectField(
        'Regional:',
        coerce=int,
        validators = [
            DataRequired(message='*Campo Requerido'),
            InputRequired(message=('*Campo Requerido'))
    ])

    submit = SubmitField('Cadastrar')    