from datetime import datetime

def getHorasByData(data):
    data_fornecida = datetime.strptime(data, '%Y-%m-%d %H:%M:%S') # Converter a string de data para o formato datetime
    data_atual = datetime.now() # Obter a data e hora atual
    
    diferenca = data_atual - data_fornecida # Calcular a diferença entre as duas datas
    diferenca_em_horas = diferenca.total_seconds() / 3600 # Converter a diferença para horas

    if diferenca_em_horas < 1:
        return "Menos de uma hora"
    elif diferenca_em_horas < 2:
        return "Há cerca de uma hora"
    else:
        print(diferenca_em_horas)
        return f"Há {int(diferenca_em_horas)} horas"