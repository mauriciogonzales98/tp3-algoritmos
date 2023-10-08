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
    self.estadoLocal = ""

class Promociones:
  def __init__(self):  
    self.codPromo = 0
    self.textoPromo = ""
    self.fechaDesdeP = ""
    self.fechaHastaP = ""
    self.diasSemana = [0]*7
    self.estadoPromo = ""
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

def formatearPromociones(regPromo):
  regPromo.codPromo = str(regPromo.codPromo).ljust(1)
  regPromo.textoPromo = regPromo.textoPromo.ljust(200)
  regPromo.fechaDesdeP = str(regPromo.fechaDesdeP).ljust(10)
  regPromo.fechaHastaP = str(regPromo.fechaHastaP).ljust(10)
  regPromo.diasSemana = str(regPromo.diasSemana).ljust(7)
  regPromo.estadoPromo = regPromo.estadoPromo.ljust(10)
  regPromo.codLocal = str(regPromo.codLocal).ljust(1)

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
  regUsuario.codUsuario = 1
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
  #global regUsuario
  email = input("ingrese su email: ")
  print("ingrese una contraseña de hasta 8 caracteres: ")
  contrasena = getpass()

  if buscarUsuario(email) == -1 and len(contrasena) == 8:
    tamUsuarios = os.path.getsize(afUsuarios)
    alUsuarios.seek(0)
    regUsuario = pickle.load(alUsuarios)
    tamregUsuario = alUsuarios.tell()
    codUser = tamUsuarios//tamregUsuario
    regUsuario.codUsuario = codUser + 1
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
  regUsuario = pickle.load(alUsuarios)
  if (regUsuario.tipoUsuario).rstrip() == "administrador":
    menuAdmin()
  elif (regUsuario.tipoUsuario).rstrip() == "duenolocal":
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
      clear()
      input('Adios!')

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
    print("1)Crear descuento")
    print("2)Reporte de uso de descuentos")
    print("3)Ver novedades")
    print("0)Salir")
    
    op = validarInput('0', '3')
  
    if op == '1':
      crearDesc(pos)
    elif op == "2":
      repUsoDesc()
    else:
      input("Diagramado en chapin")

# MENU CLIENTE-----------------------------------------------
def menuCliente():
  clear()
  print('1) Buscar descuentos en locales')
  print('2) Solicitar descuento')
  print('3) Ver novedades')
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
    
    if (regPromocion.estadoLocal).rstrip() == "pendiente":
      print("Promo nro: ",(regPromocion.codPromo).rstrip()," ", regPromocion.textoPromo,"Desde / Hasta ", (regPromocion.fechaDesdeP).rstrip(), (regPromocion.fechaHastaP).rstrip())
      for i in range (7):
        print("días activa: ",regPromocion.diasSemana[i])
      print("Local: ",(regPromocion.codLocal).rstrip())
      
      op= input("¿(A)prueba o (D)eniega?").upper
      while op != "A" or op != "D":
        op = input(" Ingrese A para aprobar o D para denegar")
      if op == "A":
        regPromocion.estadoLocal = "aprobada"
      else:
        regPromocion.estadoLocal = "denegada"

      alPromociones.seek(posPromo)
      pickle.dump(regPromocion,alPromociones)

def utilizacionDesc():
  print("d")

# Funciones del Dueño de Local
def crearDesc(pos):
  mostrarPromociones(pos)
  alUsuarios.seek(pos)
  regUsuario = pickle.load(alUsuarios)

  print("Ingrese el codigo de su local o -1 para salir")
  cod = int(input())
  if cod != -1:
    posLocal = buscarCodLocal(cod)
    if posLocal != -1:
      alLocales.seek(posLocal)
      regLocal = pickle.load(alLocales)
      if regLocal.codUsuario == regUsuario.codUsuario:

        print("Ingrese la descripcion de la promocion: ")
        promodesc = input()

        while len(promodesc) < 1 or len(promodesc) > 200:
          print("Descripcion no valida. Ingrese nuevamente la descripcion")
          promodesc = input()

        bandera = True
        #hoy = (datetime.datetime.today()).strftime('%d/%m/%Y')
        hoy = (datetime.datetime.today()).strftime('%d/%m/%Y')
        #hoy = datetime.datetime.strftime('%d/%m/%Y')
        hoy = datetime.datetime.strptime(str(hoy), '%d/%m/%Y')
        print("LA FECHA DE HOY ES: ", hoy)
        input()
        print("Ingrese la fecha de comienzo de la promocion en formato DD/MM/AAAA. No puede ser anterior a la fecha de hoy.")
        while bandera:
          try:
              fechaini = input()
              fechaini = datetime.datetime.strptime(fechaini, '%d/%m/%Y')
              if fechaini >= hoy:
                bandera = False
          except ValueError:
              print("La fecha no es valida. Intentelo nuevamente")

        print("Ingrese la fecha de finalizacion de la promocion en formato DD/MM/AAAA. Debe ser posterior a la fecha de inicio.")
        bandera = True
        while bandera:
          try:
            fechafin = input()
            fechafin = datetime.datetime.strptime(fechafin, '%d/%m/%Y')
            if fechafin > fechaini:
              bandera = False
          except ValueError:
            print("La fecha no es valida. Intentelo nuevamente")

        op = ' '
        dias = [0]*7
        while op != '0':
          print("Que dias esta activa la promocion? Pulse 0 para terminar.")
          print("1) Lunes")
          print("2) Martes")
          print("3) Miercoles")
          print("4) Jueves")
          print("5) Viernes")
          print("6) Sabado")
          print("7) Domingo")
          op = validarInput('0', '7')
          dias[int(op)-1] = 1


        tmaxPromo = os.path.getsize(afPromociones)
        alPromociones.seek(0)
        if tmaxPromo != 0:
          regPromo = pickle.load(alPromociones)
          tPromo = alPromociones.tell()
          codigo = tmaxPromo // tPromo
          posPromo = codigo * tPromo
        else:
          codigo = 0
          posPromo = 0

        regPromo = Promociones()
        regPromo.codPromo = codigo + 1
        regPromo.textoPromo = promodesc
        regPromo.fechaDesdeP = fechaini
        regPromo.fechaHastaP = fechafin
        regPromo.diasSemana = dias
        regPromo.estadoPromo = "Pendiente"
        regPromo.codLocal = cod
        formatearPromociones(regPromo)
        alPromociones.seek(posPromo)
        pickle.dump(regPromo, alPromociones)
        #falta guardar los datos en el registro, la funcion de formateo y dumpearlo
    else:
      print("Usted no es el dueño de este local o el codigo es incorrecto.")
      input()

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

  if hayDuenos():
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
        pos = codigo * tRegLocal
      else:
        codigo = 0
        pos = 0
      
      regLocal = Locales()
      regLocal.nombreLocal = nombre
      regLocal.ubicacionLocal = ubicacion
      regLocal.rubroLocal = rubro
      regLocal.codUsuario = codDueno
      regLocal.estadoLocal = 'A'
      regLocal.codLocal = codigo + 1
      formatearLocal(regLocal)
      alLocales.seek(pos)
      pickle.dump(regLocal, alLocales)

      print('Quiere ingresar otro local? Y/N')
      op = validarYN()

    # actualizarMapa()
    # mostrarRubros()
  else:
    print("No existen dueños de locales registrados, debe registrar al menos 1.")

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

  if not(b):
    pos = -1

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

def mostrarPromociones(pos):
  alUsuarios.seek(pos)
  regUsuario = pickle.load(alUsuarios)
  #busco locales por codigo de usuario
  alLocales.seek(0)
  while alLocales.tell() < os.path.getsize(afLocales):
    #posLocal = alLocales.tell()
    regLocal = pickle.load(alLocales)
    if (regLocal.codUsuario).rstrip() == (regUsuario.codUsuario).rstrip():
      alPromociones.seek(0)
      while alPromociones.tell() < os.path.getsize(afPromociones):
        posPromo = alPromociones.tell()
        regPromo = pickle.load(alPromociones)
        if (regPromo.codLocal).rstrip() == (regLocal.codLocal).rstrip():
          print("Descuento: ", regPromo.textoPromo,
                 "Fecha de inicio:", regPromo.fechaDesdeP, 
                 "Fecha de finalizacion: ", regPromo.fechaHastaP,
                 "Local: ", regLocal.nombreLocal,
                 "Estado: ", regPromo.estadoPromo)

def hayDuenos():
  alUsuarios.seek(0)
  b = False
  while alUsuarios.tell() < os.path.getsize(afUsuarios) and not(b):
    regUsuario = pickle.load(alUsuarios)
    if (regUsuario.tipoUsuario).rstrip() == 'duenolocal':
      b = True
  print("HAY DUEÑOS", b)
  input()
  return b
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
regPromo= Promociones()

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