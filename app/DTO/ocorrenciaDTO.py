class OcorrenciaDTO():

    def __init__(self, data, label):    
        self.data = data
        self.label = label

    def to_dict(self):
        return {'data': self.data, 'label': self.label}        