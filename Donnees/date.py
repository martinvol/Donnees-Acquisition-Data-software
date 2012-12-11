# -*- encoding: utf-8 -*-
#!/usr/bin/python

"""Functions for human readable current time"""

from time import localtime

def NOW():
    """Da lo hora en formato entendible (reimplementada)"""
    #This is a really bad way to do this
    aux = []
    outtime = ''

    for i in localtime():
        aux.append(str(i)) #['AÑO', 'MES', 'DIAS', 'HORAS', 'MINUTOS', 'SEGUNDOS', '2', '195', '0']
    outtime = aux[2] + '-' + aux[1] + '-' + aux[0] + '---' + aux[3] + 'h-' + aux[4] + 'm-' + aux[5] + 's'
    return outtime

def NOWlog():
    """Human readable current time"""
    #This is a really bad way to do this
    aux = []
    outtime = ''

    for i in localtime():
        aux.append(str(i)) #['AÑO', 'MES', 'DIAS', 'HORAS', 'MINUTOS', 'SEGUNDOS', '2', '195', '0']
    if len(aux[5]) == 1:
        aux[5] = '0' + aux[5]
    if len(aux[4]) == 1:
        aux[4] = '0' + aux[4]
    if len(aux[3]) == 1:
        aux[3] = '0' + aux[3]
    if len(aux[2]) == 1:
        aux[2] = '0' + aux[2]
    if len(aux[1]) == 1:
        aux[1] = '0' + aux[1]

    outtime = aux[3] + ':' + aux[4] + ':' + aux[5] + ' ' + aux[2] + '/' + aux[1] + '/' + aux[0]
    return outtime

#esto es un test
if __name__ == '__main__' :
    print NOWlog()
