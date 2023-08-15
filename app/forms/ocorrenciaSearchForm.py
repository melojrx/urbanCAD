from wtforms import Form, StringField, SubmitField, DateField
 
class OcorrenciaSearchForm(Form):

    numOcorrenciaSearch = StringField(
        'Número da Ocorrência:', 
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
    
    submit = SubmitField(
        'Filtrar'
    )