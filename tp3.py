#Mauricio Gonzales, Tomas Montaña, Lucio Zanella, Carlos Gabasio
from getpass import getpass
from os import system, name
import pickle
import os.path
import io
import time
import datetime

#Declaraciones de clases -------------------------------------------------
class Usuarios:
  def __init__(self):  
    self.codUsuario = 0
    self.nombreUsuario = ""
    self.claveUsuario = ""
    self.tipoUsuario = ""

class Locales:
  def __init__(self):  
    self.codLocal = 0
    self.nombreLocal = ""
    self.ubicacionLocal = ""
    self.rubroLocal = ""
    self.codUsuario = 0
    self.estadoLocal = "B"

class Promociones:
  def __init__(self):  
    self.codPromo = 0
    self.textoPromo = ""
    self.fechaDesdeP = ""
    self.fechaHastaP = ""
    self.diasSemana = [0]*7
    self.estadoLocal = ""
    self.codLocal = 0

class UsoPromos:
  def __init__(self):  
    self.codCliente = 0
    self.codPromo = 0
    self.fechaUsoPromo = ""

class Novedades:
  def __init__(self):  
    self.codNovedad = 0
    self.textNovedad = ""
    self.fechaDesdeN = ""
    self.fechaHastaN = ""
    self.tipoUsuario = ""
    self.estadoLocal = "B"

class Rubro():
  def __init__(self):
    self.rubro = ""
    self.cant = 0
#Funciones de formateo ---------------------------------------------------------

def formatearUsuario(regUsuario): 
  regUsuario.codUsuario = str(regUsuario.codUsuario).ljust(4)
  regUsuario.nombreUsuario = regUsuario.nombreUsuario.ljust(100)
  regUsuario.claveUsuario = regUsuario.claveUsuario.ljust(8)
  regUsuario.tipoUsuario = regUsuario.tipoUsuario.ljust(20)

def formatearLocal(regLocal):
  regLocal.codLocal = str(regLocal.codLocal).ljust(4)
  regLocal.nombreLocal = regLocal.nombreLocal.ljust(50)
  regLocal.ubicacionLocal = regLocal.ubicacionLocal.ljust(50)
  regLocal.rubroLocal = regLocal.rubroLocal.ljust(20)
  regLocal.codUsuario = str(regLocal.codUsuario).ljust(4)
  regLocal.estadoLocal = regLocal.estadoLocal.ljust(1)
#Funciones------------------------------------------------------------------------

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
    if pos >= 0:
      alUsuarios.seek(pos,0)
      regUsuario = pickle.load(alUsuarios)
      if contrasena == regUsuario.claveUsuario.rstrip():
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

def validarYN():
  op = input()
  while op.lower() != 'y' and op.lower() != 'n':
    print('La opcion ingresada no es valida')
    op = input()
  return (op.lower)

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

  #Inicializo el array de rubros
  rubros[0].rubro = "indumentaria"
  rubros[0].cant = 0
  rubros[1].rubro = "perfumeria"
  rubros[1].cant = 0
  rubros[2].rubro = "comida"
  rubros[2].cant = 0

#Funcion para registrar clientes
def registrarUsuario(tipoUsuario):
  global regUsuario
  email = input("ingrese su email: ")
  print("ingrese una contraseña de hasta 8 caracteres: ")
  contrasena = getpass()

  if buscarUsuario(email) == -1 and len(contrasena) == 8:
    tamUsuarios = os.path.getsize(afUsuarios)
    alUsuarios.seek(0)
    regUsuario = pickle.load(alUsuarios)
    tamregUsuario = alUsuarios.tell()
    codUser = tamUsuarios//tamregUsuario
    print(codUser)
    regUsuario.codUsuario =codUser 
    regUsuario.nombreUsuario = email
    regUsuario.claveUsuario = contrasena
    regUsuario.tipoUsuario = tipoUsuario
    formatearUsuario(regUsuario)
    alUsuarios.seek(codUser*tamregUsuario)
    pickle.dump(regUsuario,alUsuarios)
    alUsuarios.flush()
    print("Usuario creado con exito!")
  else:
    print("email o contraseña inválidos, intente de nuevo")
  input()
  clear()

#Determina qué usuario se logueó y llama al menú correspondiente -----------------------
def usuarioLogeado(pos):
  alUsuarios.seek(pos)
  if (regUsuario.tipoUsuario).rstrip() == "administrador":
    menuAdmin()
  elif(regUsuario.tipoUsuario).rstrip() == "duenolocal":
    menuDueno(pos)
  elif (regUsuario.tipoUsuario).rstrip() == "cliente":
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
    if (usuario == (regUsuario.nombreUsuario).rstrip()):
      b = True

  if not(b):
    pos = -1

  return pos
# Declarativa de los menus --------------------------------------------------

# MENU ADMINISTRADOR

def menuAdmin():
  clear()
  print("ADMINISTRADOR")
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
      registrarUsuario("duenolocal")

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

    clear()
    print("ADMINISTRADOR")
    print("Elija una opción:")
    print("1)Gestion de locales")
    print("2)Crear cuentas de dueños de locales")
    print("3)Aprobar/Denegar solicitud de descuento")
    print("4)Gestion de novedades")
    print("5)Reporte de utilización de descuentos")
    print("0)Salir")
    print("seleccione una opción")
    op = validarInput("0","5")


def gestionarLocales():
  print("a) Crear locales")
  print("b) Modificar local") 
  print("c) Eliminar local")
  print("d) Mapas de locales")
  print("e) Volver")

  op = input("opción: ")

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

    op = input("opción: ")

# MENU DUEÑO de LOCAL----------------------------------------
def menuDueno(pos):
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
      op = ' '
      while op != 'd':
        clear()
        print("Elija una opcion:")
        print("1)Gestión de Descuentos")
        print('    a)Crear descuento para mi local\n')
        print('    b)Modificar descuento de mi local')
        print('    c)Eliminar descuento de mi local\n')
        op = validarInput('a', 'd')
        if op == "a":
          crearDesc(pos)
        elif op == "b":
          modDesc()
        elif op == "c":
          elimDesc()
        op = validarInput('a', 'd')
    elif op == "2":
      adPedDesc()
    else:
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

def adSolDesc():
  alPromociones.seek(0)
  tamPromociones = os.path.getsize(afPromociones)
  while alPromociones < tamPromociones:
    posPromo = alPromociones.tell()
    regPromocion = pickle.load(alPromociones)
    
    if regPromocion.estadoLocal == "pendiente":
      print("Promo nro: ",regPromocion.codPromo," ", regPromocion.textoPromo,"Desde / Hasta ", regPromocion.fechaDesdeP, regPromocion.fechaHastaP)
      for i in range (7):
        print("días activa: ",regPromocion.diasSemana[i])
      print("Local: ",regPromocion.codLocal)
      
      op= input("¿(A)prueba o (D)eniega?").upper
      while op != "A" or op != "D":
        op = input(" Ingrese A para aprobar o D para denegar")
      if op == "A":
        regPromocion.estadoLocal = "aprobada"
      else:
        regPromocion.estadoLocal = "denegada"
      
      


def utilizacionDesc():
  print("d")


# Funciones del Dueño de Local
def crearDesc(pos):
  mostrarDescuentos(pos)
  alUsuarios.seek(pos)
  regUsuario = pickle.load(alUsuarios)

  print("Ingrese el codigo de su local o -1 para salir")
  cod = int(input())
  if cod != -1:
    posLocal = buscarCodLocal(cod)
    alLocales.seek(posLocal)
    regLocal = pickle.load(alLocales)
    if regLocal.codUsuario == regUsuario.codUsuario:

      print("Ingrese la descripcion de la promocion: ")
      promodesc = input()

      while len(promodesc) < 1 or len(promodesc) > 200:
        print("Descripcion no valida. Ingrese nuevamente la descripcion")
        promodesc = input()

      print("Ingrese la fecha de comienzo de la promocion en formato DD/MM/AAAA. No puede ser anterior a la fecha de hoy.")
      bandera = True
      while bandera: 
        fechaini = input()
        datetime.datetime.strptime(fechaini, '%d/%m/%Y')
        hoy = datetime.datetime.today()
        if fechaini >= hoy.strptime(hoy, '%d/%m/%Y'):
          bandera = False
        else:
          print("La fecha no es valida. Intentelo nuevamente")

      print("Ingrese la fecha de finalizacion de la promocion en formato DD/MM/AAAA. Debe ser posterior a la fecha de inicio.")
      bandera = True
      while bandera:
        fechafin = input()
        datetime.datetime.strptime(fechafin, '%d/%m/%Y')
        if fechafin > fechaini:
          bandera = False
        else:
          print("La fecha no es valida. Intentelo nuevamente")
      #falta guardar los datos en el registro, la funcion de formateo y dumpearlo
    else:
      print("Usted no es el dueño de este local o el codigo es incorrecto.")

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

def gestionarLocales():
  print("a) Crear locales")
  print("b) Modificar local") 
  print("c) Eliminar local")
  print("d) Mapas de locales")
  print("e) Volver")

  op = input("opción: ")

  while op != "e":
    clear()
    if op == 'a':
      crearLocal()

    elif op == 'b':
      modificarLocal()

    elif op == 'c':
      eliminarLocal()

    else:
      mapaLocales()

    if op == "e":
      clear()

    print("a) Crear locales")
    print("b) Modificar local") 
    print("c) Eliminar local")
    print("d) Mapas de locales")
    print("e) Volver")
    op = input("opción: ")

def crearLocal():

  op = 'y'
  while op == 'y':
    clear()
    mostrarLocales()

    nombre = checkNombreLocal()

    print('Ingrese ubicacion:')
    ubicacion = input()
    while len(ubicacion)<1 or len(ubicacion)>50:
      print("La ubicacion es muy larga")
      ubicacion = input()

    codDueno = checkCodigoDueno()

    print('Ingrese rubro:')
    rubro = rubroLocales()

    tmaxLocal = os.path.getsize(afLocales)
    alLocales.seek(0)
    if tmaxLocal != 0:
      regLocal = pickle.load(alLocales)
      tRegLocal = alLocales.tell()
      codigo = tmaxLocal // tRegLocal
    else:
      codigo = 0
    print("CODIGO ", codigo)
    
    regLocal = Locales()
    regLocal.nombreLocal = nombre
    regLocal.ubicacionLocal = ubicacion
    regLocal.rubroLocal = rubro
    regLocal.codUsuario = codDueno
    regLocal.estadoLocal = 'A'
    regLocal.codLocal = codigo
    formatearLocal(regLocal)
    pickle.dump(regLocal, alLocales)

    print('Quiere ingresar otro local? Y/N')
    op = validarYN()

  # actualizarMapa()
  # mostrarRubros()

def modificarLocal():
  clear()
  if os.path.getsize(afLocales)<=0:
    print('No hay locales cargados')
    input('Presione ENTER')
  else:
    mostrarLocales()
    print("Ingrese el codigo del local que se desea modificar:")
    cod = int(input())
    res = buscarCodLocal(cod)
    while res < 0:
      print("El codigo no existe, ingrese otro:")
      cod = int(input())
      res = buscarCodLocal(cod)

    alLocales.seek(res)
    regLocal = pickle.load(alLocales)

    if (regLocal.estadoLocal).rstrip() != 'A':
      print("Este local esta desactivado, deasea reactivar el local? Y/N")
      op = validarYN()
      if op == 'y':
        regLocal.estadoLocal = 'A'
      
    if regLocal.estadoLocal == 'A':
      print("Quiere modificar el nombre? Y/N")
      op = validarYN()
      if op == 'y':
        nombre = checkNombreLocal()
        regLocal.nombreLocal = nombre
  
      print("Quiere modificar la ubicacion? Y/N")
      op = validarYN()
      if op == 'y':
        print("Ingrese la nueva ubicacion:")
        ubicacion = input()
        while len(ubicacion)<1 or len(ubicacion)>50:
          print("La ubicacion es muy larga")
          ubicacion = input()
        regLocal.ubicacionLocal = ubicacion
  
      print("Quiere modificar el rubro? Y/N")
      op = validarYN()
      if op == 'y':
        regLocal.rubroLocal = rubroLocales()
        calcularRubros()


  
      print("Quiere modificar el codigo del dueño? Y/N")
      op = validarYN()
      if op == 'y':
        print("Ingrese el nuevo codigo de usuario:")
        codDueno = checkCodigoDueno()
        regLocal.codUsuario = codDueno

      formatearLocal(regLocal)
    else:
      print('No se puede modificar los datos de un local inactivo')

def eliminarLocal():
  clear()
  if os.path.getsize(afLocales)<=0:
    print('No hay locales cargados')
    input('Presione ENTER')
  else:
    mostrarLocales()
    print("Ingrese el codigo del local que desea eliminar o -1 para salir:")
    cod = int(input())
    res = buscarCodLocal(cod)
    if res != -1 and cod != -1:
      alLocales.seek(res)
      regLocal = pickle.load(alLocales)
      if regLocal.estadoLocal == 'A':
        print("Deasea eliminar el local? Y/N")
        op = validarYN()
        if op == 'y':
          regLocal.estadoLocal = 'B'
          calcularRubros()
          

def calcularRubros():
  alLocales.seek(0)
  tmLocales = os.path.getsize(afLocales)
  rubros[0].cant = 0
  rubros[1].cant = 0
  rubros[2].cant = 0
  while alLocales.tell() < tmLocales:
    regLocal = pickle.load(alLocales)
    if (regLocal.rubroLocal).rstrip() == "indumentaria" and (regLocal.estadoLocal).rstrip == 'A':
      rubros[0].cant += 1
    if (regLocal.rubroLocal).rstrip() == "perfumeria" and (regLocal.estadoLocal).rstrip == 'A':
      rubros[1].cant += 1
    if (regLocal.rubroLocal).rstrip() == "comida" and (regLocal.estadoLocal).rstrip == 'A':
      rubros[2].cant += 1

def checkNombreLocal():
  print("Ingrese el nombre del local a crear")
  local = input()
  res = buscarLocal(local)
  while (len(local) < 1 or len(local)>50) and res != -1: 
    print("Este nombre no esta disponible, ingrese otro por favor")
    local = input()
    res = buscarLocal(local)
  return local

def buscarLocal(nombre):
  b = False
  alLocales.seek(0)
  tmLocales = os.path.getsize(afLocales)
  while (alLocales.tell() < tmLocales) and not(b):
    pos = alLocales.tell()
    regLocal = pickle.load(alLocales)
    if (nombre == (regLocal.nombreLocal).rstrip()):
      b = True

  if not(b):
    pos = -1

  return pos

def checkCodigoDueno():
  mostrarUsuarios()
  print("Ingrese el codigo del dueño del local")
  cod = int(input())
  res = buscarCodUsuario(cod)
  alUsuarios.seek(res)
  regUsuario = pickle.load(alUsuarios)
  while res == -1 or ((regUsuario.tipoUsuario).rstrip() != "duenolocal"):
    print("El codigo ingresado no existe, ingrese otro")
    cod = int(input())
    res = buscarCodUsuario(cod)
  return int(regUsuario.codUsuario)

def buscarCodUsuario(cod):
  alUsuarios.seek(0)
  regUsuario = pickle.load(alUsuarios)
  tUsuario = alUsuarios.tell()
  tmUsuarios = os.path.getsize(afUsuarios)
  cantUsuarios = tmUsuarios // tUsuario
  alUsuarios.seek(0)

  inicio = 0
  fin = cantUsuarios
  b = False
  while alUsuarios.tell()<tmUsuarios and not(b):
    mid = (inicio + fin)//2
    alUsuarios.seek(mid*tUsuario)
    pos = alUsuarios.tell()
    regUsuario = pickle.load(alUsuarios)
    if int(regUsuario.codUsuario) == cod:
      b = True
    elif cod < int(regUsuario.codUsuario):
      fin = mid - 1
    else:
      inicio = mid + 1

  return pos

def buscarCodLocal(cod):
  alLocales.seek(0)
  regLocal = pickle.load(alLocales)
  tLocal = alLocales.tell()
  tmLocales = os.path.getsize(afLocales)
  cantLocales = tmLocales // tLocal
  alLocales.seek(0)

  inicio = 0
  fin = cantLocales
  b = False
  while alLocales.tell()<tmLocales and not(b):
    mid = (inicio + fin)//2
    alLocales.seek(mid*tLocal)
    pos = alLocales.tell()
    regLocal = pickle.load(alLocales)
    if int(regLocal.codLocal) == cod:
      b = True
    elif cod < int(regLocal.codLocal):
      fin = mid - 1
    else:
      inicio = mid + 1

  return pos

def mostrarLocales():
  alLocales.seek(0)
  print("Codigo Local\t Nombre\t Ubicacion\t Rubro\t Codigo Dueño\t Estado")
  while alLocales.tell() < os.path.getsize(afLocales):
    regLocal = pickle.load(alLocales)
    print((regLocal.codLocal).rstrip(), (regLocal.nombreLocal).rstrip(), (regLocal.ubicacionLocal).rstrip(), (regLocal.rubroLocal).rstrip(), int(regLocal.codUsuario), (regLocal.estadoLocal).rstrip(), sep='\t', end='\n')

def mostrarUsuarios():
  alUsuarios.seek(0)
  tmUsuarios = os.path.getsize(afUsuarios)
  print("Codigo Usuario\t Nombre\t Tipo usuario\t")
  while alUsuarios.tell() < tmUsuarios:
    regUsuario = pickle.load(alUsuarios)
    print((regUsuario.codUsuario).rstrip(), (regUsuario.nombreUsuario).rstrip(), (regUsuario.tipoUsuario).rstrip(), sep='\t', end='\n')

def rubroLocales():
  print("Elija el rubro del local")
  print("1) Perfumeria")
  print("2) Indumentaria")
  print("3) Comida")
  op = validarInput('1', '3')
  if op == '1':
    r = "perfumeria"
  elif op == '2':
    r = "indumentaria"
  else:
    r = "comida"
  #actualizarRubros(r, id)
  return r

def mostrarDescuentos(pos):
  print("a\n")
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#- Programa principal -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

# Apertura de archivos --------------------------------------------------------

#abro archivo usuario
afUsuarios = "C:\\Users\\PC\\Desktop\\TP3 algoritmos\\usuarios.dat"
if not os.path.exists(afUsuarios):
  alUsuarios = open(afUsuarios, "w+b")
else:
  alUsuarios = open(afUsuarios, "r+b")
regUsuario = Usuarios()

#abro archivo locales
afLocales = "C:\\Users\\PC\\Desktop\\TP3 algoritmos\\locales.dat"
if not os.path.exists(afLocales):
  alLocales = open(afLocales, "w+b")
else:
  alLocales = open(afLocales, "r+b")
regLocal = Locales()

#Abro archivo Promociones

afPromociones = "C:\\Users\\PC\\Desktop\\TP3 algoritmos\\promociones.dat"
if not os.path.exists(afPromociones):
  alPromociones = open(afPromociones, "w+b")
else:
  alPromociones = open(afPromociones, "r+b")
regPromocion = Promociones()


# Abro archivo Locales
afLocales = "C:\\Users\\PC\\Desktop\\TP3 algoritmos\\locales.dat"
if not os.path.exists(afLocales):
  alLocales = open(afLocales, "w+b")
else:
  alLocales = open(afLocales, "r+b")

regLocal = Locales()

global rubros 
rubros= [Rubro()]*3
cargaAuxiliar()
calcularRubros()
# Menu General
print("Bienvenido!")
print("Ingrese una opcion: ")
print("1) Ingresar con usuario registrado.")
print("2) Registrarse como cliente.")
print("3) Salir.")

op = validarInput("1", "3")

if op == '1':
  res = login()
  if res != -1:
    usuarioLogeado(res)
  else:
    print("La contraseña se ha ingresado incorrectamente demasiadas veces")
    input()

elif op == '2':
  registrarUsuario("cliente")

else:
  clear()
  print("Adios!")
  input()