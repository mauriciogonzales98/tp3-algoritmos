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

#Funciones de formateo ---------------------------------------------------------

def formatearUsuario(regUsuario): 
    regUsuario.codUsuario = str(regUsuario.codUsuario).ljust(4)
    #regUsuario.codUsuario = regUsuario.codUsuario.ljust(4)
    regUsuario.nombreUsuario = regUsuario.nombreUsuario.ljust(100)
    regUsuario.claveUsuario = regUsuario.claveUsuario.ljust(8)
    regUsuario.tipoUsuario = regUsuario.tipoUsuario.ljust(20)

#---------------------------------------------
#Funciones

#Funcion clear para limpiar la consola, verifica que SO se esta usando
def clear():
  if name == 'nt':
    _ = system('cls')
  else:
    _ = system('clear')


#Funcion de login
def login():
  global alUsuarios
  res = -1
  intentos = 0
  while res < 0 and intentos < 3:

    print('Ingrese usuario:')
    usuario = input()
    print('Ingrese contraseña:')
    contrasena = getpass()
    pos = buscarUsuario(usuario)
    print("LA POSICION ES:", pos)
    input()
    if pos >= 0:
      alUsuarios.seek(pos,0)
      regUsuario = pickle.load(alUsuarios)
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

#Validacion de las opciones de los menus --------------------------------
def validarInput(desde, hasta):
  op = input()
  while op < desde or op > hasta:
    print('La opcion ingresada no es valida')
    print('Ingrese otra opcion')
    op = input()
    clear()
  return op

#Cargo datos arbitrarios para testear ------------------------------------
def cargaAuxiliar():
  #adm
  global alUsuarios
  regUsuario.codUsuario = 0
  regUsuario.nombreUsuario = "admin@shopping.com"
  regUsuario.claveUsuario = "12345"
  regUsuario.tipoUsuario = "administrador"
  alUsuarios.seek(0)
  formatearUsuario(regUsuario)
  pickle.dump(regUsuario, alUsuarios)
  alUsuarios.flush()

#Funcion para registrar clientes
def registrarUsuario(tipoUsuario):
  email = input("ingrese su email")
  regUsuario=
  


#Determina que usuario se logeo y llama al menu correspondiente -----------------------
def usuarioLogeado():
	if regUsuario.tipoUsuario == "administrador":
		menuAdmin()
	elif regUsuario.tipoUsuario == "duenolocal":
		menuDueno()
	elif regUsuario.tipoUsuario == "cliente":
		menuCliente()

#Busca un usuario en el archivo de usuarios. Barrido secuencial. -----------------------
def buscarUsuario(usuario):
  b = False
  alUsuarios.seek(0)
  tmUsuario = os.path.getsize(afUsuarios)
  #global regUsuario
  while (alUsuarios.tell() < tmUsuario) and not(b):
    pos = alUsuarios.tell()
    regUsuario = pickle.load(alUsuarios)
    #ACA ES EL ERROR, posiblemente formateo
    print(regUsuario.nombreUsuario, usuario)
    input()
    if (usuario == regUsuario.nombreUsuario):
      print("BANDERITA")
      input()
      b = True

  if not(b):
    pos = -1

  return pos

# Declarativa de los menus --------------------------------------------------
  # MENU ADMINISTRADOR
def menuAdmin():
  clear()
  print("Elija una opción:")
  print("1)Gestion de locales")
  print("2)Crear cuentas de dueños de locales")
  print("3)Aprobar/Denegar solicitud de descuento")
  print("4)Gestion de novedades")
  print("5)Reporte de utilización de descuentos")
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
      print("ok")
      clear()
      print('Adios!')

    print("seleccione una opción")
    op = validarInput("0","5")
def gestionarLocales():
  print("a) Crear locales")
  print("b) Modificar local") 
  print("c) Eliminar local")
  print("d) Mapas de locales")
  print("e) Volver")

  op = str(input("opción: "))

  while op != "e":
        clear()
        if op == "a":
          crear_locales()

        if op == "b":
          mod_local()

        if op == "c":
         eliminar_local()
            
        if op == "d":
          mapa_locales()

        if op == "e":
          clear()

        op = str(input("opción: "))

# MENU DUEÑO de LOCAL----------------------------------------

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

# MENU CLIENTE-----------------------------------------------
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

#Funciones del Administrador----------------------------------
def gestionarLocales():
  print("a")

def crearCuentasDuenos():
  print("b")

def adSolDesc():
  print("c")

def utilizacionDesc():
  print("d")


# Funciones del Dueño de Local
def crearDesc():
  print("e")

def modDesc():
 print("f")

def elimDesc():
  print("g")

def adPedDesc():
  print("h")

def repUsoDesc():
  print("i")

#Funciones del Cliente
def registroCliente():
  print("j")

def buscoDescuento():
  print("k")

def solicitoDescuento():
  print("l")

def verNovedades():
  print("m")


#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#- Programa principal -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#


#abro archivo usuario
afUsuarios = "C:\\Users\\PC\\Desktop\\TP3 algoritmos\\usuarios.dat"
if not os.path.exists(afUsuarios):
  alUsuarios = open(afUsuarios, "w+b")
else:
  alUsuarios = open(afUsuarios, "r+b")

regUsuario = Usuarios()

#Cargo algunos datos basicos para el funcionamiento del programa
cargaAuxiliar()

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
    input()

elif op == '2':
  registrarCliente()

else:
  clear()
  print("Adios!")
  clear()




def crear_locales():

  str(input("Nombre del local: "))                
  str(input("Ubicación: "))
  str(input("rubro: "))
  int(input("código de usuario: "))








        
                       





