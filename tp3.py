from getpass import getpass
from os import system
import pickle
import os.path
import io
import time
import datetime

#Declaraciones de clases
class Usuarios:
     def __init__(self):  
        self.codUsuario = 0
        self.nombreUsuario = ['']*100
        self.claveUsuario = ['']*8
        self.tipoUsuario = ['']*20

class Locales:
     def __init__(self):  
        self.codLocal = 0
        self.nombreLocal = ['']*50
        self.ubicacionLocal = ['']*50
        self.rubroLocal = ['']*50
        self.codUsuario = 0
        self.estadoLocal = "B"

class Promociones:
     def __init__(self):  
        self.codPromo = 0
        self.textoPromo = ['']*200
        self.fechaDesdeP = ['']*10
        self.fechaHastaP = ['']*10
        self.diasSemana = [0]*7
        self.estadoLocal = ['']*10
        self.codLocal = 0

class UsoPromos:
     def __init__(self):  
        self.codCliente = 0
        self.codPromo = 0
        self.fechaUsoPromo = ['']*50

class Novedades:
     def __init__(self):  
        self.codNovedad = 0
        self.textNovedad = ['']*200
        self.fechaDesdeN = ['']*10
        self.fechaHastaN = ['']*10
        self.tipoUsuario = ['']*20
        self.estadoLocal = "B"