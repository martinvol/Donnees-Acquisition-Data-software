# -*- encoding: utf-8 -*-
#!/usr/bin/python

"""Este modulo lanza todos los procesos del programa, maneja todas las funciones
y administra todos los recursos.'
El programa se encarga de levantar datos del puerto serie de forma constante.
Esos datos los sube a internet, los guarda en la base de datos, hace graficos
de los datos de la base de datos y esos datos enviarlos por mail. En caso de 
emergencia envia un email a una API de las companias de mensageria, el mensage enviado
llega a encargado de la instalacion describiendo el problema."""

#Importamos todo lo que necesitamos:
if __name__ == "__main__":
    from twisted.internet import gtk2reactor # for gtk-2.0
    gtk2reactor.install()

from twisted.internet import reactor

from models.conf import direccion
from os.path import join

from models import serie, lista
from twisted.internet.defer import inlineCallbacks, Deferred

from pylab import setp
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
#plt.subplots_adjust(hspace=.3, left=.5)
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk import FigureCanvasGTK as FigureCanvas

from server import server

from subprocess import Popen

#El toolkit grafico
#import pygtk
from gtk import glade
#import gobject

#from sys import argv

#if "-f" in argv:
#    import serial_fake as serial
#else:
#    import serial
#    print "Puerto"
#    help(serial.Serial)
    
#Modulo para hacer multi-threading (multi-hilos)
#import threading

#El modulo para multipreceso

#El modulo time para poder pausar el programa
import time

#La comunicacion con el puerto serie

#Modulos que son partes del programa
#El modulo par alas fechas
#from date import *
from datetime import datetime, timedelta
from multiprocessing import Process, Queue
from Queue import Empty

from sys import stdout, argv

from twisted.internet import reactor
from Mailing import mail
from grafico import AbreParsea
from twisted.internet.threads import deferToThread
#from threading import Thread

#El modulo de la base de datos

#El modulo para leer mails

#El modulo que abre los graficos
#from grafico import AbreParsea

#El modulo que lee los mails




#ACA DECLARABA SERIAL
Serial_ = serie.Serial_

class ATratar(object):
    "Esto transforma el diccionario en un objeto"
    actual = None
    viejo = None
    viejo_viejo = None
    tiempo = None
    
    def __init__(self, kargs):
        self.chota = 3
        for i in kargs.keys():
            setattr(self, i, kargs[i])
        if self.grafico:
            self.grafico = self.grafico(self) #despues hay que pasarle el color
        
    def sacar_ultima(self):
        if self.viejo is None:
            self.viejo = self.actual
            return self.actual
        elif self.viejo == self.actual:
            return None #No es necesario actualizar
        else:
            self.viejo_viejo = self.viejo
            self.viejo = self.actual
            return self.actual

class ReactorObj:
    reactor = "a"

class Gui(object):
    def __init__(self, app):
        """'Constructor' la objeto de la interfaz grafica."""
        self.companias = {0:"@sms.movistar.net.ar", 1:"@sms.cmail.com.ar"}
        self.app = app
        self.glade = glade.XML("Interfaz.glade")
        self.glade.signal_autoconnect(self)
        self.glade.get_widget("window1").maximize()
        self.temp_label = self.glade.get_widget("label5")  #temperatura
        self.ph_label = self.glade.get_widget("label6")  #pH
        self.o2_label = self.glade.get_widget("label7")  #O2
        self.label10 = self.glade.get_widget("label10")#Recirculacion
        self.label11 = self.glade.get_widget("label11")#Caldera
        self.entry1 = self.glade.get_widget("entry1")#celular
        self.entry2 = self.glade.get_widget("entry2")#e-mail
        self.checkbutton1 = self.glade.get_widget("checkbutton1")
        self.checkbutton2 = self.glade.get_widget("checkbutton2")
        self.combobox1 = self.glade.get_widget("combobox1") #compania celular
        self.contenedor = self.glade.get_widget ("vbox8") #contenedor
        self.combobox1.set_active(0)
        self.image1 = self.glade.get_widget("image1")#Recirculacion
        self.image2 = self.glade.get_widget("image2")#Recirculacion
        
        self.entry1.set_text(''.join(open('conf/telefono')).replace('\n',''))
        self.entry2.set_text(''.join(open('conf/email')).replace('\n',''))

        self.show_all()

    def graficodia(self, widget):
        print "grafico día"
        Popen(["python", "grafico-nomail.py"])

    def grafico(self, widget):
        print "grafico siempre"

        Popen(["python", "grafico-nomail.py", "nodia"])
        
    def stop(self, _bool):
        self.image1.set_sensitive(_bool)
        self.image2.set_sensitive(not _bool)

    def update_label(self, nombre, a_widget):
        if a_widget.nombre == "caldera":
                if a_widget.actual: self.label11.set_text("ON")
                else: self.label11.set_text("OFF")
        elif a_widget.actual and a_widget.widget:
            getattr(self, '%s_label' % nombre).set_text(a_widget.actual + a_widget.unidad)
            

    def show_all(self):
        self.glade.get_widget("window1").show_all()

    def get_celphone(self):
        """Devuelve la direccion de mail puesta en la GUI"""
        return self.entry1.get_text() + self.companias[self.combobox1.get_active()]

    def get_email(self):
        """Devuelve el numero de celular puesto en la GUI"""
        return self.entry2.get_text()
        
    def salir(self,widget, signal):
        """Salir"""
        from twisted.internet import reactor
        reactor.stop()

def deco(*Arg):
    def _deco(f):
        def inner(*args, **kwargs):
            from twisted.internet import reactor
            reactor.callLater(Arg[0], inner, *args, **kwargs)
            pause = Arg[1]
            if pause is None:
                pause = args[0].is_stoped
            if not pause:
                return f(*args, **kwargs)
        return inner
    return _deco

class App (object):
    """Esta clase se convertira en el proceso de la interfaz grafica"""
    lista_de_valores = None

    def __init__(self, connection, q, q1):         #inicializa toda la interfaz grafica
        from twisted.internet import reactor
        self.q = q
        self.q1 = q1
        self.connection = connection
        self.connection.app = self
        self.gui = Gui(self)
        self.comand = ""
        self.is_stoped = True
        self.graficando = False
        self.mandar = True

        for name in lista_de_valores:
            obj = ATratar(name)    
            setattr(self, name["nombre"], obj)
            setattr(self.gui, 'graph_%s' % name, obj.grafico)
            if obj.grafico and not "-g" in argv:
                obj.grafico.app = self
                self.gui.contenedor.add(obj.grafico.canvas)
                reactor.callLater(.1, obj.grafico.on_redraw_timer)
        self.gui.show_all()

        reactor.callLater(10, self.mandar_mails) #tiempo de aranque de mails
        reactor.callWhenRunning(self.conseguir_datos)
        reactor.callWhenRunning(self.refresh)
        reactor.callWhenRunning(self.subir)
        reactor.callWhenRunning(self.sms)
        #reactor.callWhenRunning(self.test)

    #@deco(.4, None)
    #def test(self):
        #print self.gui.checkbutton2.get_active()
        #print self.ph.actual
        #print self.o2.actual
        #print self.temp.actual
        #print self.caldera.actual

    def stop(self, _bool):
        self.gui.stop(_bool)
        #cambiar la gui
        self.is_stoped = _bool

    @deco(60*60*2, False)
    def mandar_mails(self):
        self.graficando = False
        def inner_blocking_code():
            AbreParsea(lista_de_valores)
            mail(self.gui.get_email(), "Grafico de las instalaciones " 
            + str(datetime.now().strftime("%H:%M:%S %d/%m/%y")), "Se registra un nivel de O2 de %s mg/l, un nivel de ph de %s y una temperatura de %sºC" % (self.ph.actual,                 self.o2.actual,self.temp.actual), attach0=join(direccion, "grafico.png"))
            print "mandé mail"
            
        def termine(arg):
            self.graficando = False

        if self.gui.checkbutton2.get_active():
            done = lambda arg: stdout.write(str(arg) + " terminé" + "\n")
            failed = lambda err: err.printTraceback()#stdout.write(str(arg.getErrorMessage()) + " fallé" + "" + "\n")

            d = deferToThread(inner_blocking_code)
            d.addCallbacks(done, failed)
            d.addCallbacks(termine)

    @deco(.1, None)
    @inlineCallbacks    
    def subir(self):
        from twisted.internet import reactor
        for i in lista_de_valores:
            i = i["nombre"]
            j = getattr(self, i)
            a_subir = j.sacar_ultima()
            if a_subir or a_subir == 0:
                a_subir = str(a_subir)
                if not self.graficando:
                    self.q.put((j.nombre, j.actual, j.tiempo, j.viejo_viejo))
                #print a_subir, j.nombre
                self.connection.sendConnected(a_subir, j.nombre, j.tiempo.strftime("%H:%M:%S_%d/%m/%y"))
            yield
    
    @deco(.1, False)
    @inlineCallbacks    
    def conseguir_datos(self):
        try:
            self.valor = self.q1.get(block=False)
            #print self.valor, "App" rs232
        except Empty:
            self.valor = ()
            #print "No estaba lista la Queue"
        yield
        if self.valor == "fallo":
            self.stop(True)
        elif self.valor:
            #print self.valor
            self.stop(False)
            for i in lista_de_valores:
                i = i["nombre"]
                if i in self.valor:	
                    #print self.valor
                    #if i == "caldera":
                    #    print i, self.valor[i]
                    j = getattr(self, i)
                    j.actual = self.valor[i]
                    j.tiempo = datetime.now()
                else:
                    pass
                yield

    @deco(.1, None)
    @inlineCallbacks
    def refresh(self):
        for i in lista_de_valores:
            nombre = i["nombre"]
            a_widget =  getattr(self, nombre)#.actual
            self.gui.update_label(nombre, a_widget)
            yield
#        self.gui.update_labels(self.valor)

    @deco(1, None)
    @inlineCallbacks
    def sms(self):
        mande = False
        for i in lista_de_valores:
            yield
            if i["dato"] and self.mandar and self.gui.checkbutton1.get_active():
                j = getattr(self, i["nombre"])
                if float(j.actual) <  j.minimo or float(j.actual) >  j.maximo:
                    print "Mando SMS", j.nombre
                    self.mandar_sms(j)
                    mande = True
                    reactor.callLater(10*60, self.semaforo_sms)
        if mande: self.mandar = False
        yield
                
    def mandar_sms(self, nombre):
        self.mandar_mails_alerta()
        def inner_blocking_code():
            mail(self.gui.get_celphone(), "Alerta " 
                + str(datetime.now().strftime("%H:%M:%S %d/%m/%y")), "Se registra un nivel de %s de %s, estos valores   son peligrosos." % (nombre.nombre, nombre.actual))
            
        def termine(arg):
            self.graficando = False

        if self.gui.checkbutton2.get_active():
            done = lambda arg: stdout.write(str(arg) + " terminé" + "\n")
            failed = lambda err: err.printTraceback()#stdout.write(str(arg.getErrorMessage()) + " fallé" + "" + "\n")

            d = deferToThread(inner_blocking_code)
            d.addCallbacks(done, failed)
            d.addCallbacks(termine)
    
    
    def semaforo_sms(self):
        self.mandar = True

    def mandar_mails_alerta(self):
        self.graficando = False
        def inner_blocking_code():
            AbreParsea(lista_de_valores)
            mail(self.gui.get_email(), "Alerta " 
                + str(datetime.now().strftime("%H:%M:%S %d/%m/%y")), "Se registra un nivel de O2 de %s mg/l, un nivel de ph de %s y una temperatura de %sºC" % (self.ph.actual,                 self.o2.actual,self.temp.actual), attach0=join(direccion, "grafico.png"))
            print "mandé mail, con alerta y gráfico"
            
        def termine(arg):
            self.graficando = False

        done = lambda arg: stdout.write(str(arg) + " terminé" + "\n")
        failed = lambda err: err.printTraceback()#stdout.write(str(arg.getErrorMessage()) + " fallé" + "" + "\n")

        d = deferToThread(inner_blocking_code)
        d.addCallbacks(done, failed)
        d.addCallbacks(termine)


def p1(q, ):
    import time
    import log
    import datetime
    bases = {}
    while True:
#        print "Process 2"
        vino = q.get()
        nombre = vino[0]
        if not nombre in bases:
            #print vino
            #lo instacio y lo meto en el dict            
            bases[nombre] = log.DataBase(nombre)
        #if nombre == "caldera":
            #print vino[3], vino[1]
        #j.nombre, j.actual, j.tiempo, j.viejo_viejo
        #print vino[3], vino[1]
        #bases[nombre].escribira(vino[3], vino[2] - datetime.timedelta(seconds=.01))    
        bases[nombre].escribira(vino[1], vino[2])
        #actualizo esa base

def rs232(q1, Serial_):
    """Esta funcion es la encargada de tomar los datos del puerto serie
    y envialos a todos los otrs procesos, discriminando si son valores o estados"""
    def abrir():
        while True:
            try:
                time.sleep(1)
                print 'buscando puerto...'
                for i in xrange(20):
                    try:
                        retornar = Serial_("/dev/ttyUSB%s" % str(i) , 1200, timeout = .2)
                        print 'Puerto encontrado en', i
                        return retornar
                        print "encontre"
                    except :
                        pass
            except:
                pass

    ser = abrir()

    counter = 0
    maximo = 0
    while 1:
        counter += 1
        try:
            try:
                dato = ser.mis_datos()
                #print dato
                #print dato
            except OSError:
                ser.close()             #si el sistema operativo nos niega el acceso al puerto
                ser.open()              #lo reinicimamos

            #print dato, dato
            if dato is None:
                print dato, "falló"
                q1.put("fallo")
                ser = abrir()
            elif "caldera" in dato:
                q1.put(dato)
            elif not q1.full() and counter > maximo and dato != {}:
                #print dato ,"dato"
                if "caldera" in dato:
                    print dato
                q1.put(dato)
                counter = 0
                if q1.qsize() > 2:
                    maximo += 1
                    #esto regula el tamaño de la Queue
            if q1.full():
                print "canal de comunicación rebalzó"
                q1 = Queue()
        except IndexError:
            ser = abrir()


def main():
    q = Queue()
    p = Process(target=p1, args=(q,))
    p.daemon = True
    p.start()

    q1 = Queue()
    p = Process(target=rs232, args=(q1, Serial_))
    p.daemon = True
    p.start()    
    
    from twisted.internet import reactor
    factory = server.ChatFactory()
    reactor.listenTCP(7777, factory)
    app = App(factory, q, q1)
    app.lista_de_valores = lista_de_valores
    reactor.run()
    p.terminate()

lista_de_valores = lista.lista_de_valores


if __name__ == "__main__":
    #Si el programa se esta ejecutando(no es importado)
    #se ejecuta
    """Inicia el programa"""
    main()
