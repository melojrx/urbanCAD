from validate_docbr import CPF
from wtforms import ValidationError

class ValidaCpf(object):
    def __init__(self, message=None):
        if message is None:
            message = 'Ops. Não nos parece um CPF válido.'
        self.message = message

    def __call__(self, form, field):
        cpf = CPF()
        if not cpf.validate(field.data):
            raise ValidationError(self.message)