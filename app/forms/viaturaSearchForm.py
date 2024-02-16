from wtforms import Form, StringField, SelectField, SubmitField

class ViaturaSearchForm(Form):

    txtCodigoSearch = StringField(
        'Código:',
        render_kw={"placeholder": "Código da viatura"}
        )

    txtPlacaSearch = StringField(
        'Placa:',
        render_kw={"placeholder": "Placa da viatura"}
        )   

    txtDescricaoSearch = StringField(
        'Descrição:',
        render_kw={"placeholder": "Descrição da viatura"}
    )        

    idInstituicaoSearch = SelectField(
        'Instituição',
        coerce=int
    )

    idTipoPatrulhaSearch = SelectField(
        'Tipo Patrulha',
        coerce=int
    )

    submitSearch = SubmitField('Pesquisar')