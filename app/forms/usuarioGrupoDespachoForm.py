from wtforms import Form, SelectField, SubmitField
from wtforms.validators import DataRequired, InputRequired

class UsuarioGrupoDespachoForm(Form):  

    usuarios = SelectField(
        'Usuário',
        coerce=int,
        validators = [
            DataRequired(message='*Campo Requerido'),
            InputRequired(message=('*Campo Requerido'))
    ])

    gruposDeDespacho = SelectField(
        'Grupo de Despacho',
        coerce=int,
        validators = [
            DataRequired(message='*Campo Requerido'),
            InputRequired(message=('*Campo Requerido'))
    ])

    submit = SubmitField('Cadastrar')    