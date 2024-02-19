from wtforms import Form, HiddenField, StringField, SubmitField
from wtforms.validators import InputRequired, Length
 
class InstituicaoForm(Form):

    id = HiddenField('id')

    txtInstituicao = StringField(
        'Nome da Instituição:',
        render_kw={"placeholder": "Nome da Instituição"},
        validators = [
            InputRequired(message=('*Campo Requerido')),
            Length(max=50, message='A senha deve ter no máximo %(max)d caracteres')
        ])

    txtSigla = StringField(
        'Sigla da Instituição:',
        render_kw={"placeholder": "Sigla da Instituição"},
        validators = [
            InputRequired(message=('*Campo Requerido')),
            Length(max=10, message='A senha deve ter no máximo %(max)d caracteres')
        ])
    
    submit = SubmitField('Cadastrar')