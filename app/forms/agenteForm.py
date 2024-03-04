from wtforms import Form, HiddenField, SelectField, SubmitField
from wtforms.validators import DataRequired, InputRequired

class AgenteForm(Form):  

    id = HiddenField('id')

    usuario = SelectField(
        'Usuário:',
        coerce=int,
        validators = [
            DataRequired(message='*Campo Requerido'),
            InputRequired(message=('*Campo Requerido'))
    ])

    idInstituicao = SelectField(
        'Instituição:',
        coerce=int,
        validators = [
            DataRequired(message='*Campo Requerido'),
            InputRequired(message=('*Campo Requerido'))
    ])

    submit = SubmitField('Cadastrar') 


    def __init__(self, *args, **kwargs):
        super(AgenteForm, self).__init__(*args, **kwargs)

        # Preencher o campo usuario se houver um agente associado
        if 'obj' in kwargs and kwargs['obj'] and kwargs['obj'].usuario:
            self.usuario.data = kwargs['obj'].usuario.id