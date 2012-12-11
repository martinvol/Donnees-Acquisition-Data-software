#! /usr/bin/env python
# -*- coding: utf-8 -*-


import pygame

from urllib2 import urlopen

from twisted.internet import reactor
from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import ClientFactory

#Initializes pygame
pygame.init()
pygame.font.init()
pygame.display.set_caption("SCADA | Proyecto Tilapia")
SIZE = (1024, 550)
screen = pygame.display.set_mode(SIZE)


#Load all the resources from files
font = pygame.font.Font(None,32)
fondo = pygame.image.load("static/fondo.png").convert_alpha()
valvulaSI = pygame.image.load("static/valvulaSI.bmp").convert_alpha()
valvulaNO = pygame.image.load("static/valvulaNOb.bmp").convert_alpha()
bombaSI = pygame.image.load("static/bombaSI.bmp").convert_alpha()
bombaNO = pygame.image.load("static/bombaNO.bmp").convert_alpha()
aireSI = pygame.image.load("static/aireSI.bmp").convert_alpha()
aireNO = pygame.image.load("static/aireNO.bmp").convert_alpha()
flechaDE = pygame.image.load("static/flecha_dcha.png").convert_alpha()
flechaIZ = pygame.image.load("static/flecha_izq.png").convert_alpha()


class Sprite(pygame.sprite.Sprite):
    def __init__(self, imagen, lugar):
        pygame.sprite.Sprite.__init__(self)
        self.image = imagen
        self.rect = self.image.get_rect()
        self.rect.clamp_ip(screen.get_rect())
        self.rect[0] = lugar[0]
        self.rect[1] = lugar[1]

class Indicador(pygame.sprite.Sprite):
    def __init__(self, lugar, medicion, color=(255,255,255)):
        pygame.sprite.Sprite.__init__(self)
        self.medicion = medicion
        self.color = color
        self.actualizar('0')
        self.rect = self.image.get_rect()
        self.rect[0] = lugar[0]
        self.rect[1] = lugar[1]
    def actualizar(self,puntaje):
        self.text = self.medicion + puntaje
        self.image = font.render(self.text,1,self.color)

def decorador(f):
    def sacar(*arg, **karg):
        #print 'entre a', f.__name__
        try:
            return f(*arg, **karg)
        except :
            print 'Error en', f.__name__
    return sacar

def parseador(X):
    """Transforma el strig X en una lista de 3 elementos"""
    try:
        X = str(X)
        X = X.replace('.', '')
        Ph = X[:2] + "." + X[2]
        O2 = X[3:5] + "." + X[5]
        Temp = X[6:8]+ "." + X[8]
        lista = [Ph,O2,Temp]
        #print lista, 'ALALALLA'
        return lista
    except:
        print 'FAIL'

urlopen = decorador(urlopen)

#Initializes all the objects
#TODO, this should be made automatically with a loop
flecha01 = Sprite( imagen=flechaDE, lugar=(750,414) ) #del filtro
flecha02 = Sprite( imagen=flechaDE, lugar=(750,254) ) #caldera
valvula01 = Sprite( imagen=valvulaNO, lugar=(62,277) ) #esta es de reserva
valvula02 = Sprite( imagen=valvulaNO, lugar=(170,319) ) #esta es de del tanque
valvula03 = Sprite( imagen=valvulaNO, lugar=(739,477) ) #esta filtra
valvula04 = Sprite( imagen=valvulaNO, lugar=(558,398) ) #esta no filtra (izquierda)
valvula05 = Sprite( imagen=valvulaNO, lugar=(907,398) ) #esta no filtra (derecha)
valvula06 = Sprite( imagen=valvulaNO, lugar=(818,273) ) #frio (izquierda)
valvula07 = Sprite( imagen=valvulaNO, lugar=(663,273) ) #calor (derecha)
valvula08 = Sprite( imagen=valvulaNO, lugar=(230,395) ) #valvula de bomba01
valvula09 = Sprite( imagen=valvulaNO, lugar=(230,475) ) #valvula de bomba02
bomba01 = Sprite( imagen=bombaNO, lugar=(381,400) ) #bomba principal
bomba02 = Sprite( imagen=bombaNO, lugar=(381,477) ) #bomba de emergencia
aire01 = Sprite( imagen=aireNO, lugar=(474,142) ) #aireador
indicadorPh = Indicador(lugar=(400,244), medicion='Ph: ')
indicadorO2 = Indicador(lugar=(400,294), medicion='02: ')
indicadorTemp = Indicador(lugar=(400,344), medicion='Temp: ')

#Instances all the objects
#TODO, this should be made automatically with a loop
GrupoSprite = pygame.sprite.Group()
GrupoSprite.add(valvula01, valvula02)#De donde entro el agua
GrupoSprite.add(valvula03, valvula04, valvula05)
GrupoSprite.add(valvula06, valvula07)
GrupoSprite.add(valvula08, valvula09)
GrupoSprite.add(bomba01, bomba02)
GrupoSprite.add(aire01)
GrupoSprite.add(flecha01,flecha02)
GrupoFont = pygame.sprite.Group()
GrupoFont.add(indicadorPh, indicadorO2, indicadorTemp)

#Inicializar simulacion
screen.blit(fondo,(0,0))
clock = pygame.time.Clock()
running = True

#Definimos funciones
def EntraAgua(reserva=False, tanque=False):
    if reserva:
        valvula01.image = valvulaSI
        valvula02.image = valvulaNO
    elif tanque:
        valvula01.image = valvulaNO
        valvula02.image = valvulaSI

def recirculando(filtrar=False, renovar=False):
    if filtrar:
        flecha01.image = flechaIZ
        valvula03.image = valvulaSI
        valvula04.image = valvula05.image = valvulaNO
    elif renovar:
        flecha01.image = flechaDE
        valvula03.image = valvulaNO
        valvula04.image = valvula05.image = valvulaSI

def caldera(calor=False, frio=False, apagar=False):
    if frio:
        flecha02.image = flechaIZ
        flecha02.rect[0] = 750
        flecha02.rect[1] = 254
        valvula06.image = valvulaNO
        valvula07.image = valvulaSI
    elif calor:
        flecha02.image = flechaDE
        flecha02.rect[0] = 750
        flecha02.rect[1] = 254
        valvula06.image = valvulaSI
        valvula07.image = valvulaNO
    elif apagar:
        flecha02.rect[0] = 1000
        flecha02.rect[1] = 1000
        valvula06.image = valvulaNO
        valvula07.image = valvulaNO

def bomba(normal=False, emergencia=False):
    if normal:
        bomba01.image = bombaSI
        bomba02.image = bombaNO
        valvula08.image = valvulaSI
        valvula09.image = valvulaNO
    elif emergencia:
        bomba01.image = bombaNO
        bomba02.image = bombaSI
        valvula08.image = valvulaNO
        valvula09.image = valvulaSI

def aire(prendido=False, apagado=False):
    if prendido:
        aire01.image = aireSI
    elif apagado:
        aire01.image = aireNO

#definimos estados
@decorador
def estados_caldera(caldera_st=None):
    if 'e' in caldera_st:
        caldera(calor=True)
    elif 'd' in caldera_st:
        caldera(frio=True)
    else:
        print 'Error en el estado de la caldera'

@decorador
def stados_agua(agua_st=None):
    if 'a' in agua_st:
        EntraAgua(tanque=True)
    elif 'b' in agua_st:
        EntraAgua(reserva=True)
    else:
        pass
        #print 'Error en el estado deL agua'

@decorador
def stados_filtro(filtro_st=None):
    #print filtro_st
    if 'c' in filtro_st:
        recirculando(renovar=True)
        caldera(apagar=True)
        EntraAgua(tanque=True)
        return False
    elif 'z' in filtro_st:
        recirculando(filtrar=True)
        return True
    else:
        print "Error en el filtro"

@decorador
def estados_bomba(bomba_st=None):
    #print bomba_st
    if 'n' in bomba_st:
        bomba(normal=True)
    elif 'j' in bomba_st:
        bomba(emergencia=True)
    else:
        print 'Error en el estado de la bomba'

@decorador
def oxigeno(valor):
    valor = float(valor)
    #print valor, 'ALLALALALAL'
    if valor < 6:
        aire(prendido=True)
    elif valor > 8:
        aire(apagado=True)
@decorador
def actualizar_estado(valores):
    valores2 = valores1 = valores #urlopen('http://volteck.net/proyecto/devolver-todo.php').read()
    lista = parseador(valores2)
    oxigeno(lista[1])
    estados_bomba(valores)
    if stados_filtro(valores):
        #print 'ENTRO'
        estados_caldera(valores)
        stados_agua(valores)

    indicadorPh.actualizar(lista[0])
    indicadorO2.actualizar(lista[1] + " mg/m3")
    indicadorTemp.actualizar(lista[2] + " ºC".decode("utf-8"))


def loop(valores):
    for event in pygame.event.get():
          if (event.type == pygame.KEYUP) or (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_ESCAPE):
                reactor.stop()
          elif event.type == pygame.QUIT:
            reactor.stop()
#    keystate = pygame.key.get_pressed()
#    if keystate[pygame.K_LEFT]:
#        flecha02.rect[0] -= 1
#    if keystate[pygame.K_RIGHT]:
#        flecha02.rect[0] += 1
#    if keystate[pygame.K_UP]:
#        flecha02.rect[1] -= 1
#    if keystate[pygame.K_DOWN]:
#        flecha02.rect[1] += 1
#    #print flecha02.rect


#    #print lista[1]

    actualizar_estado(valores)

    #   2-Avanzar simulacion
    clock.tick(20)

    #   3-Dibujar estado actual
    GrupoSprite.clear(screen, fondo)
    GrupoSprite.draw(screen)
    GrupoSprite.update()

    GrupoFont.clear(screen, fondo)
    GrupoFont.draw(screen)
    GrupoSprite.update()
    pygame.display.flip() #esto siempre al final

def main():
    while running:
        loop()

class AppScada:
    def __init__(self):
        reactor.callLater(1, self.lala)
        self.valores = {"ph": "00.0", "o2":"00.0", "temp":"00.0", "caldera":"e", "SCADA":"zbn"}

    def lala(self):
        a_pasar = "%s%s%s%s%s" % (self.valores["ph"], self.valores["o2"], self.valores["temp"], self.valores["caldera"], self.valores["SCADA"])
        #print a_pasar
        loop(a_pasar)
        #loop("8.38.031.9zean")
        reactor.callLater(.1, self.lala)

class MyProtocol(LineReceiver):
    def lineReceived(self, line):
        #print "line received"
        line = line.split(" ")
        #print line ESTO LO TILDE
        if line[0] != "caldera":
            self.factory.app.valores[line[0]] = line[1]
        else:
            self.factory.app.valores[line[0]] = "e" if line[1] == "True" else "d"

    def connectionMade(self):
        print "Connection made"

    def connectionLost(self, reason):
        print "Connection Lost"

class MyFactory(ClientFactory):
    protocol = MyProtocol

    def __init__(self, app):
        self.app = app

    #def buildProtocol(self, addr):
    #    self.instance = self.protocol()
    #    return self.instance



class check_class:
    def __init__(self, Y):
        self.connection = Y
        reactor.callLater(2, self.check)

    def check(self):
        print self.connection.state
        if self.connection.state != "connected":
            print "intento reconectar"
            self.connection = connect()
        reactor.callLater(2, self.check)


if __name__ == '__main__':
    App = AppScada()
    factory = MyFactory(App)
    def connect():
        return reactor.connectTCP("localhost", 7777, factory)

    check_class(connect())
    reactor.run()

"""if __name__ == '__main__':
    App = AppScada()
    def initial_connect():
        def connect():
            print "conecto"
            factory = MyFactory(App)
            check = check_class(reactor.connectTCP("localhost", 7777, factory))
        reactor.callLater(1, check.check, connect)
        return connect
    x = initial_connect()


    reactor.run()"""
