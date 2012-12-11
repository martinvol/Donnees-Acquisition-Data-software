# -*- encoding: utf-8 -*-
#!/usr/bin/python

"""This module is a high level API for a SQLlite database"""

import time
import sqlite3
from os.path import join
from models.conf import direccion

class DataBase(object):
    """This class represents a strorable object. It is instances ones per value
     API will be translataed in upcommin releases"""
    def __init__(self, dato):
        """El 'constructor' del objeto,
        dato es un string y asi se llamara la tabla a crear"""
        self.dato = dato
        self.Nombredato = dato #base tiene que ser un string
        self.check = True
        self.iniDataBase()
        self.actualizar = True

    def iniDataBase(self):
        """Opens a connection with the database, in the tables doesn't exist, creates them'"""
        #TODO Creates one table per value, this is super bad
        self.conn = sqlite3.connect(join(direccion, 'DataBase/example'), detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        self.c = self.conn.cursor()
        self.c.execute("SELECT * FROM sqlite_master WHERE type='table'")
        self.New = False
        for i in self.c:
            #print self.dato in i
            if self.dato in i:
                self.New = True
#        print self.New
        if self.New:
            pass
        else:
            self.c.execute('''create table %s
                      (valor real, date timestamp)''' % self.Nombredato)
            print 'No hay tabla, y la creo'

    def escribira(self, valor, fecha):
        """Saves value into a table with *fecha* as date, if fecha is not given
        it is stored with the system time"""


        #print valor
        if self.actualizar:
            self.datoviejo =  valor
            self.actualizar =  False
            return False, valor

        if self.datoviejo != valor:
            try:
                #self.iniDataBase()
                self.c.execute('insert into %s values (?,?)' % (self.Nombredato),(valor, fecha))
                self.conn.commit()
                self.c.execute('select * from %s' % self.Nombredato)
                self.a = self.c.fetchone()
                self.CerrarDataBase()
                self.datoviejo = valor
                return True, valor
            except:
                self.iniDataBase()
                print "falle al commitear la base de datos"
        else:
            #print 'era igual', self.dato, valor
            return False, valor

#       time.sleep(20)

    def CerrarDataBase(self):
        """Closes the database"""
        self.c.close()



#TODO from there all this code is old and should be thrown away
baseURL = ('http://volteck.net/proyecto/parametros.php?o=', '&ph=', '&temp=', '&horario=')


def Subir(entrada):
    """Parsea una lista y sube sus valors al servidor
    a partir de el string baseURL"""
    O2, ph, temp = entrada[0], entrada[1], entrada[2]
#    print O2, ph, temp
    if O2[0] or ph[0] or temp[0]:
        subir = True
    else:
        subir = False
    if subir:
        #print O2[1], ph[1],temp[1]
        parametrosURL = baseURL[0] + str(ph[1]) + baseURL[1] + str(O2[1]) + baseURL[2] + str(temp[1]) + baseURL[3] + NOWlog().replace("/","-").replace(" ","_")[:8]
        #print parametrosURL
        try:
            urlopen(parametrosURL)
        except:
            print 'no pude subir'

def instanciar():
    """Retorna los objetos de todas las clases en una tupla"""
    a = DataBase('O2')
    b = DataBase('ph')
    c = DataBase('temp')
    return a,b,c

def Dale(entrada,a,b,c):
    """Llama a Subir() pasandole los datos de escribira, uno por cada clase"""
    try:
        Subir((
        a.escribira(entrada[0]),
        b.escribira(entrada[1]),
        c.escribira(entrada[2])))
    except: pass

def test():
    """Esta funcion prueba la conexion y la base de datos"""
    import random
    a = DataBase('O2')
    b = DataBase('ph')
    c = DataBase('temp')

    while 1:
        try:
            Subir((
            a.escribira(8 + round(random.random(),1)),
            b.escribira(7 + round(random.random(),1)),
            c.escribira(31 + round(random.random(),1))))
        except: #es un None, los None no tiene posiciones
            print 'no hay datos'


if __name__ == '__main__':
#   Ejecutamos el test
    test()


