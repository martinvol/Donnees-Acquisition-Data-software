# -*- encoding: utf-8 -*-
#!/usr/bin/python

"""Este modulo se encarga de generar los graficos de todas las tablas 
en la base de datos y guardarlos a disco"""

from models.lista import lista_de_valores

#Importamos todo lo relativo a graficos y matematica
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import date
import pylab
import matplotlib
import matplotlib.dates
import datetime
from matplotlib.dates import DateFormatter
from pylab import *

#Importamos el modulo para acceder a la base de datos
import sqlite3

from os.path import join
from models.conf import direccion


import gtk
import sys, time


class bar:
    def __init__(self, objetos):
        self.counter = 0
        self.lista = list()
        for i in objetos:
            if i["nombre"] != "caldera" and i["grafico"]: self.counter +=1
        self.window = gtk.Window()
        self.window.set_title ("Generador de historial")
        self.window.resize (300, 100)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.deletable = True
        self.window.connect("delete_event", self.cerrar)
        self.window.set_icon_from_file("grafico.png")
        self.container = gtk.VBox()
        self.label0 = gtk.Label(str="Cargando historial de Base de Datos")
        self.container.add (self.label0)
        for i in xrange(self.counter):
            bar = gtk.ProgressBar()
            self.container.add(bar)
            self.lista.append(bar)
#        self.bar.show()
        self.window.add(self.container)
        self.window.show_all()

    def cerrar (*args):
        sys.exit()
    def progressa(self, data, i):
        it= iter(data)
        #widget = bar()
        largo = it.__length_hint__()
        c=0
        for v in it:
            c+=1
            self.lista[i].set_fraction(float(c)/largo)
            while gtk.events_pending():
                gtk.main_iteration()
            yield(v)
        
    def ocultar(self):
        self.window.hide()
        while gtk.events_pending():
            gtk.main_iteration()
                
plt.subplots_adjust(hspace=.29, left=.07, right=.99, top=.95,bottom=.05 )

def DesdeAca(base):
    #print len (base)
    base.reverse()
    #print base[0][1], base[-1][1]
    """Busca la fecha de un d"""
    #base.reverse()
    print base[0][1]
    for n,j in enumerate(base):
        fecha = j[1]
        if datetime.datetime.now() - fecha > datetime.timedelta(days=1):
            #print fecha
            #import sys
            #sys.exit()
            #print "less"
            return n
    return n

def abrelabase(tabla):
    from os import system
    #system("cp DataBase/example example2")
    conn = sqlite3.connect(join(direccion, 'DataBase/example'), detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    c = conn.cursor()
    c.execute('select * from %s' % tabla)
#    row = c.fetchone()
#    print type(row[1])
    lista = list(c) 
    #print len(lista)   
    c.close()
    conn.close()
    #system("rm DataBase/example2")
    return lista

def AbreParsea(objetos, dia=True):
    fig = pylab.gcf()
    if dia:
        fig.canvas.set_window_title('Historial de producción diario')
    else:
        fig.canvas.set_window_title('Historial de producción')

    progressa = bar(objetos)
    for j, i in enumerate(objetos):
        if i["nombre"] != "caldera" and i["grafico"]:
            array0 = array1 = array2 =np.array([])

            archivo = abrelabase(i["nombre"])
            #print len(archivo)

            #print usar
            #print archivo[0][1] > archivo[-1][1]
            if dia:
                usar = DesdeAca(archivo) #esto estaba arriba de if
                archivo = archivo[:usar]
            print archivo[0][1], "-"+ str(archivo[-1][1])
            #print  len(archivo)

        #    print archivo
        
            for k in progressa.progressa(archivo, j):
                numero = k[0]
                fecha = k[1]
                array0 = np.append(array0, numero)
                array1 = np.append(array1, fecha)
            #if i["nombre"] == "temp":
            #    archivo_caldera =  abrelabase("caldera")
            #    if dia:
            #        usar_caldera = DesdeAca(archivo_caldera) #esto estaba arriba de if
            #        archivo_caldera = archivo[:usar_caldera]
            #    array0_caldera = array1_caldera =np.array([])
                temp_max = array0.max()
                temp_min = array0.min()
                #for k in progressa.progressa(archivo_caldera, j):
                #    numero = k[0]
                #    fecha = k[1]
                #    if numero:
                #        array0_caldera = np.append(array0_caldera, (numero * temp_max)+1)
                #    else:
                #        array0_caldera = np.append(array0_caldera, (numero + temp_min)-1)
                #    array1_caldera = np.append(array1_caldera, fecha)

 
            
            array2 = list()
            array2.append(array1[0])
            array2.append(array1[-1])

            var = i["medio"]

            ax = plt.subplot(310 + j +1 )
            if not j:
                ax.set_title('Grafico de la instalaciones: '+ date.NOWlog())
            plt.plot()
            #if i["nombre"] == "temp":
            #    print "caldera"
            #    plt.plot_date(mpl.dates.date2num(array1_caldera), array0_caldera, linestyle='-', marker='.',xdate=.8, c="g");

            plt.plot_date(mpl.dates.date2num(array2),[var,var],linestyle='--',marker='',c="r")
            plt.grid()
            plt.plot_date(mpl.dates.date2num(array1), array0, linestyle='-', marker='',xdate=.8, c=i["color"]);
            ax.xaxis.set_major_formatter(DateFormatter('%H:%M %D'))
            #print i   
            plt.ylabel(u"%s [%s]" % (i["formal"], i["unidad"]) )
            ylim(array0.min() + -1 if array0.min() - 1 < i["medio"] else i["medio"] -1, array0.max() + 1)
            

            plt.setp(ax.get_xticklabels(),'rotation',40,fontsize=8)
            


    #plt.savefig(join(direccion, "grafico.png") ,dpi=1024/8)
    progressa.ocultar()
    del progressa
    plt.show()


"""
    array0 = array1 = array2 =np.array([])r


    archivo =  tablas = abrelabase('o2')
    usar = DesdeAca(archivo)
    archivo = abrelabase('o2')[usar:]
    
    for i in archivo:
        rfecha = str(i[1])
        numero = i[0]
        #print i
        #print rfecha[-4:], rfecha[-7:-5], rfecha[-10:-8], rfecha[0:2], rfecha[3:5], rfecha[6:8]  
        fecha = i[1]
        #print fecha
        array0 = np.append(array0, numero)
        array1 = np.append(array1, fecha)

    array2 = list()
    array2.append(array1[0])
    array2.append(array1[-1])
    var = 7
    ax = plt.subplot(312)
    plt.plot_date(mpl.dates.date2num(array2),[var,var],linestyle='--',marker='',c='r')
    plt.grid()
    plt.plot_date(mpl.dates.date2num(array1), array0, linestyle='-', marker='',xdate=.8,c='y')
    ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))    
    plt.setp(ax.get_xticklabels(),'rotation',40,fontsize=8)
    ylim(0, 20)
    plt.ylabel(u"Oxigeno[mg/l]") 



    array0 = array1 = array2 =np.array([])
    archivo = abrelabase('ph')
    usar = DesdeAca(archivo)
    archivo = abrelabase('ph')[usar:]

    for i in archivo:
        rfecha = str(i[1])
        numero = i[0]
#        print i
#        print rfecha[-4:], rfecha[-7:-5], rfecha[-10:-8], rfecha[0:2], rfecha[3:5], rfecha[6:8]  
        fecha = i[1]
#        print fecha
        array0 = np.append(array0, numero)
        array1 = np.append(array1, fecha)

    array2 = list()
    array2.append(array1[0])
    array2.append(array1[-1])
    var = 7
    ax = plt.subplot(313)
    plt.plot_date(mpl.dates.date2num(array2),[var,var],linestyle='--',marker='',c='r')
    plt.xlabel("Horas")
    plt.grid()
    plt.plot_date(mpl.dates.date2num(array1), array0, linestyle='-', marker='',xdate=.8,c='g');
    ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))    
    plt.setp(ax.get_xticklabels(),'rotation',40,fontsize=8)
    ylim(0, 14)
    plt.ylabel("Ph")
    plt.savefig('grafico1.png' ,dpi=1024/8)
    plt.show()
    print 'Grafico listo'
"""



if __name__ == '__main__':
    from sys import argv
    if "nodia" in argv:
        AbreParsea(lista_de_valores, False)
    else:
        AbreParsea(lista_de_valores)
#    print DesdeAca(abrelabase('ph'))
    plt.show()
