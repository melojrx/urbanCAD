from wtforms import Form, SubmitField, BooleanField, DateField, TimeField
from flask_bootstrap import Bootstrap
 
class DeteccaoSearchForm(Form):
  
    dataInicioSearch = DateField(
        'Início', 
        format='%Y-%m-%d',
        render_kw={"placeholder": "dd/mm/aa"}
    )


    dataFimSearch = DateField(
        'Fim', 
        format='%Y-%m-%d',
        render_kw={"placeholder": "dd/mm/aa"}
    )

    isPlacaSearch = BooleanField(
        'Apenas registros com placa:'
    )

    submit = SubmitField(
        'Filtrar'
    )