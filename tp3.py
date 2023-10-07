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

#Validacion de las opciones de los menus
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
	if regUsuarios.tipoUsuario == "administrador":
		menuAdministrador()
	elif regUsuarios.tipoUsuario == "duenolocal":
		menuDueno()
	elif regUsuarios.tipoUsuario == "cliente":
		menuCliente()

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

# Declarativa de los menus

def menuAdmin():
  clear()
  print("Elija una opcion:")
  print("1)Gestion de locales")
  print("2)Crear cuentas de dueños de locales")
  print("3)Aprobar/Denegar solicitud de descuento")
  print("4)Gestion de novedades")
  print("5)Reporte de utilizacion de descuentos")
  print("0)Salir")
  op = validarInput('0', '5')

  while op != '0':

    if op == '1':
      gestionarLocales()
    elif op == '2':
      crearCuentasDuenos()
    elif op == '3':
      adSolDesc()
    elif op == "4":
      print("codificado en chapín")
    elif op == '5':
      utilizacionDesc()
    else:
      clear()
      print('Adios!')


def menuDueno():
  op = ''
  while op != '0':
    clear()
    print("Elija una opcion:")
    print("1)Gestión de Descuentos")
    print("2)Aceptar / Rechazar pedido de descuento")
    print("3)Reporte de uso de descuentos")
    print("0)Salir")
    
    op = validarInput('0', '3')
  
    if op == '1':
    #Submenu
      while op != 'd':
        clear()
        print("Elija una opcion:")
        print("1)Gestión de Descuentos")
        print('    a)Crear descuento para mi local\n',
              '   b)Modificar descuento de mi local')
        print('    c)Eliminar descuento de mi local\n')
        if op == "a":
          crearDesc()
        elif op == "b":
          modDesc()
        elif op == "c":
          elimDesc()
        elif op == "2":
          adPedDesc()
        elif op == "3":
          repUsoDesc()

def menuCliente():
  clear()
  print('1) Registrarme')
  print('2) Buscar descuentos en locales')
  print('3) Solicitar descuento')
  print('4) Ver novedades')
  print('0) Salir')
  op = validarInput('0', '4')

  while op != '0':

    if op == "1":
      registroCliente()
    elif op == "2":
      buscoDescuento()
    elif op == "3":
      solicitoDescuento()
    elif op == "4":
      verNovedades()

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