from wtforms import Form, StringField, SelectField, SubmitField

class InstituicaoSearchForm(Form):

    txtInstituicaoSearch = StringField(
        'Nome:',
        render_kw={"placeholder": "Nome da instituição"}
        )

    txtSiglaSearch = StringField(
        'Sigla:',
        render_kw={"placeholder": "Sigla da instituição"}
        )   

    submitSearch = SubmitField('Consultar')