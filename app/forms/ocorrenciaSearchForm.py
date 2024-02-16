from wtforms import Form, StringField, SubmitField, DateField, SelectField
 
class OcorrenciaSearchForm(Form):

    numOcorrenciaSearch = StringField(
        'Número da Ocorrência', 
        render_kw={"placeholder": "Número da Ocorrência"}
    )
    
    dataInicioSearch = DateField(
        'Início', 
        format='%d/%m/%Y',
        render_kw={"placeholder": "dd/mm/aa"}
    )

    dataFimSearch = DateField(
        'Fim', 
        format='%d/%m/%Y',
        render_kw={"placeholder": "dd/mm/aa"}
    )

    statusSearch = SelectField(
        'Status',
        coerce=int,
        )
    
    submit = SubmitField(
        'Consultar'
    )