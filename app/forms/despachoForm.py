from wtforms import Form, StringField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, InputRequired
 
class DespachoForm(Form):

    ocorrencia = StringField()
    idRegiao = StringField()
    
    despacharPara = SelectMultipleField(
        'Despachar Para:',
        [
            DataRequired(message='*Campo Requerido'),
            InputRequired(message=('Por favor, informe seu Nome.'))
        ]
    )

    submit = SubmitField('Despachar')