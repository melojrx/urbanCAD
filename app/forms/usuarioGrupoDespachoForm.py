from wtforms import Form, HiddenField, SelectField, SubmitField
from wtforms.validators import DataRequired, InputRequired

class UsuarioGrupoDespachoForm(Form):  

    id = HiddenField('id')

    usuario = SelectField(
        'Usuário:',
        coerce=int,
        validators = [
            DataRequired(message='*Campo Requerido'),
            InputRequired(message=('*Campo Requerido'))
    ])

    grupoDespacho = SelectField(
        'Grupo de Despacho:',
        coerce=int,
        validators = [
            DataRequired(message='*Campo Requerido'),
            InputRequired(message=('*Campo Requerido'))
    ])

    submit = SubmitField('Cadastrar')

    def __init__(self, *args, **kwargs):
        super(UsuarioGrupoDespachoForm, self).__init__(*args, **kwargs)

        # Preencher o campo usuario
        if 'obj' in kwargs and kwargs['obj'] and kwargs['obj'].usuario:
            self.usuario.data = kwargs['obj'].usuario.id

        # Preencher o campo grupoDespacho
        if 'obj' in kwargs and kwargs['obj'] and kwargs['obj'].grupoDespacho:
            self.grupoDespacho.data = kwargs['obj'].grupoDespacho.id