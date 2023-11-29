from wtforms.widgets import TextArea, HiddenInput
from wtforms import FileField, Form, StringField, SubmitField
from wtforms.validators import InputRequired, Length

class DespachoObservacaoForm(Form):

    idDespachoHistorico = StringField(
        widget=HiddenInput())

    observacao = StringField(
        'Observação:',
        widget=TextArea(),
        render_kw={"placeholder": "Insira aqui observações sobre a ocorrência"},
        validators = [
            InputRequired(message=('*Campo Requerido')),
            Length(max=500, message='A senha deve ter no máximo %(max)d caracteres')
        ])
    
    file = FileField(
        'Insira uma foto:'
        )

    submit = SubmitField('Cadastrar')    