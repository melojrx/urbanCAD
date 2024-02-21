from wtforms import Form, SelectField, StringField, SubmitField


class GrupoDespachoSearchForm(Form):  

    txtNomeSearch = StringField(
        'Grupo de Despacho:',
    )

    idRegionalSearch = SelectField(
        'Regional:',
        coerce=int,
    )

    submitSearch = SubmitField('Consultar')    