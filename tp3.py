from getpass import getpass
from os import system, name
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

ruta = "C:\Users\PC\Desktop\TP3 algoritmos"
afUsuarios = ruta
if not os.path.exists(afUsuarios):
  alUsuarios = open(afUsuarios, "w+b")
else:
  alUsuarios = open(afUsuarios, "r+b")

#Funciones

#Funcion clear para limpiar la consola, verifica que SO se esta usando
def clear():
  if name == 'nt':
    _ = system('cls')
  else:
    _ = system('clear')


#Funcion de login
def login():
  res = -1
  intentos = 0
  while res < 0 and intentos < 3:

    print('Ingrese usuario:')
    usuario = input()
    print('Ingrese contraseña:')
    contrasena = getpass()
    pos = buscarUsuario(usuario)

    if pos >= 0:
      alUsuarios.seek(pos)
      regUsuario = Usuarios()
      if contrasena == regUsuario.claveUsuario:
        res = pos
      else:
        clear()
        print('Contraseña incorrecta')
    else:
      clear()
      print('Usuario inexistente')
    intentos += 1

  return res

#Validarcion de las opciones de los menus
def validarInput(desde, hasta):
  op = input()
  while op < desde or op > hasta:
    print('La opcion ingresada no es valida')
    print('Ingrese otra opcion')
    op = input()
    clear()
  return op

#Funcion para registrar clientes
def registrarCliente():
  print("En construccion")

#Determina que usuario se logeo y llama al menu correspondiente
def usuarioLogeado():
  print("En construccion")

#Busca un usuario en el archivo de usuarios. Barrido secuencial.
def buscarUsuario(usuario):
  b = False
  alUsuarios.seek(0)
  regUsuario = Usuarios()
  tmUsuario = os.path.getsize(alUsuarios)

  while alUsuarios.tell() < tmUsuario and not(b):
    pos = alUsuarios.tell()
    regUsuario = pickle.load(alUsuarios)
    #No me reconoce el objeto, no se por que
    if usuario == regUsuario.nombreUsuario:
      b = True

  if not(b):
    pos = -1

  return pos

#Programa principal


#abro archivo usuario


print("Bienvenido!")
print("Ingrese una opcion: ")
print("1) Ingresar con usuario registrado.")
print("2) Registrarse como cliente.")
print("3) Salir.")

op = validarInput("1", "3")

if op == '1':
  res = login()
  if res != -1:
    usuarioLogeado()
  else:
    print("La contraseña se ha ingresado incorrectamente demasiadas veces")

elif op == '2':
  registrarCliente()

else:
  print("Adios!")
  clear()