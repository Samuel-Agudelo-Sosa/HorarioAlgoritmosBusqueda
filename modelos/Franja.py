class Franja:

    def __init__(self, dia, inicio, fin):
        self.dia = dia
        self.inicio = inicio
        self.fin = fin



    def _hora_a_minutos(self, hora_str):
        partes = hora_str.split(':')
        return int(partes[0]) * 60 + int(partes[1])

    def inicio_minutos(self):
        return self._hora_a_minutos(self.inicio)

    def fin_minutos(self):
        return self._hora_a_minutos(self.fin)


    def se_cruza_con(self, otra_franja):
        if self.dia.lower() != otra_franja.dia.lower():
            return False
        return self.inicio_minutos() < otra_franja.fin_minutos() and otra_franja.inicio_minutos() < self.fin_minutos()

    def duracion(self):
        return (self.fin_minutos() - self.inicio_minutos()) / 60

    def __repr__(self):
        return f"Franja{self.dia} {self.inicio}-{self.fin}"