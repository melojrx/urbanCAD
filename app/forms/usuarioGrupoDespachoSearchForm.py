from wtforms import Form, HiddenField, SelectField, SubmitField
from wtforms.validators import DataRequired, InputRequired

class UsuarioGrupoDespachoSearchForm(Form):  

    usuarioSearch = SelectField(
        'Usuário',
        coerce=int
    )

    grupoDespachoSearch = SelectField(
        'Grupo de Despacho',
        coerce=int
    )

    submitSearch = SubmitField('Consultar')    