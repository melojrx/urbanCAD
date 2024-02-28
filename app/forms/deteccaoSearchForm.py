from wtforms import Form, SubmitField, BooleanField, DateField, TimeField
 
class DeteccaoSearchForm(Form):
  
    dataInicioSearch = DateField(
        'Data de Início:', 
        format='%Y-%m-%d',
        render_kw={"placeholder": "dd/mm/aa"}
    )

    horaInicioSearch = TimeField(
        'Hora Início:'
    )

    dataFimSearch = DateField(
        'Data de Fim:', 
        format='%Y-%m-%d',
        render_kw={"placeholder": "dd/mm/aa"}
    )

    horaFimSearch = TimeField(
        'Hora Fim:'
    )

    isPlacaSearch = BooleanField(
        'Apenas registros com placa:'
    )

    submit = SubmitField(
        'Consultar'
    )