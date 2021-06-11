class Carta():
    def __init__(self, n, t, i):
        self.numero = n
        if(self.numero <= 10):
            self.valor = n
        else:
            self.valor = 10
        if(t == 0):
            self.tipo = 'corazon'
        elif(t == 1):
            self.tipo = 'diamante'
        elif(t == 2):
            self.tipo = 'trebol'
        else:
            self.tipo = 'pica'
        self.id = i
