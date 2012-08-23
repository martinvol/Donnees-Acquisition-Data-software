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

plt.subplots_adjust(hspace=.16, left=.07, right=.99, top=.95,bottom=.05 )

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
    import os
    os.system("cp DataBase/example DataBase/temp15")
    conn = sqlite3.connect(join(direccion, 'DataBase/example'), detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    c = conn.cursor()
    c.execute('select * from %s' % tabla)
#    row = c.fetchone()
#    print type(row[1])
    lista = list(c) 
    #print len(lista)   
    c.close()
    conn.close()
    os.system("rm DataBase/temp15")
    return lista

def AbreParsea(objetos):
    for j, i in enumerate(objetos):
        if i["nombre"] != "caldera" and i["nombre"] != "SCADA":
            #print i["nombre"]
            array0 = array1 = array2 =np.array([])

            archivo = abrelabase(i["nombre"])
            #print len(archivo)
            usar = DesdeAca(archivo)
            #print usar
            #print archivo[0][1] > archivo[-1][1]
            archivo = archivo[:usar]
            print archivo[0][1], "-"+ str(archivo[-1][1])
            #print  len(archivo)

        #    print archivo

            for k in archivo:
                numero = k[0]
                fecha = k[1]
                array0 = np.append(array0, numero)
                array1 = np.append(array1, fecha)
            
            array2 = list()
            array2.append(array1[0])
            array2.append(array1[-1])

            var = 30

            ax = plt.subplot(310 + j +1 )
            if not j:
                ax.set_title('Grafico de la instalaciones: '+ date.NOWlog())
            plt.plot()
            plt.plot_date(mpl.dates.date2num(array2),[var,var],linestyle='--',marker='',c="r")
            plt.grid()
            plt.plot_date(mpl.dates.date2num(array1), array0, linestyle='-', marker='',xdate=.8, c=i["color"]);
            ax.xaxis.set_major_formatter(DateFormatter('%H:%M %D'))
            #print i   
            plt.ylabel(u"%s [%s]" % (i["formal"], i["unidad"]) )
            ylim(0, array0.max() + 1)

            plt.setp(ax.get_xticklabels(),'rotation',10, fontsize=8)

    plt.savefig(join(direccion, "grafico.png") ,dpi=1024/8)
    print "Grafico listo"
    
    #plt.show()


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
    AbreParsea(lista_de_valores)
#    print DesdeAca(abrelabase('ph'))
    #plt.show()
