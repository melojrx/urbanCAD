from wtforms import Form, StringField, SelectField, SubmitField

class AgenteSearchForm(Form):

    agenteSearch = StringField(
        'Agente:',
        render_kw={"placeholder": "Nome do agente"}
        )   

    idInstituicaoSearch = SelectField(
        'Instituição',
        coerce=int
    )


    submitSearch = SubmitField('Consultar')