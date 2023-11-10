from enum import Enum

class StatusOcorrenciaEnum(Enum):
    AGUARDANDO_DESPACHO = 1
    ENVIADO_PARA_DESPACHO = 2
    EM_ANDAMENTO = 3
    FINALIZADO = 4