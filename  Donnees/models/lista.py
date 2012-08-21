# -*- encoding: utf-8 -*-
#!/usr/bin/python

from widget_graficos import Graph, Graphtemp

lista_de_valores = (
    {"formal":"pH", "nombre": "ph", "color": "y", "medio":7, "maximo": 9, "minimo": 6, "unidad": "", "grafico":Graph, "widget": True, "dato":True}, #ph
    {"formal":"Temperatura","nombre": "temp", "color": "b", "medio":30, "maximo": 35, "minimo": 27, "unidad": "ºC","grafico":Graphtemp, "widget":True, "dato":True}, #temp
    {"formal":"O2", "nombre": "o2", "color": "m", "medio":10, "maximo": 200, "minimo": 3, "unidad": "mg/m³", "grafico":Graph, "widget":True, "dato":True}, #o2
    {"formal":"Tiempo Caldera", "nombre": "caldera", "grafico":"", "widget":False, "dato":False}, #caldera
    {"formal":"SCADA", "nombre": "SCADA", "grafico":"", "widget":False, "dato":False}, #caldera
    )

