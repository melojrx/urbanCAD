from wtforms import Form, StringField, SubmitField

class TipoPatrulhaSearchForm(Form):

    txtTipoPatrulhaSearch = StringField(
        'Tipo de Patrulha:',
        render_kw={"placeholder": "Tipo de Patrulha"}
    )
    
    submitSearch = SubmitField('Consultar')