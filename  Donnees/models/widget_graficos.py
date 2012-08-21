# -*- encoding: utf-8 -*-
#!/usr/bin/python

import time
from pylab import setp
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
#plt.subplots_adjust(hspace=.3, left=.5)
from matplotlib.figure import Figure
from twisted.internet.defer import inlineCallbacks, Deferred
from matplotlib.backends.backend_gtk import FigureCanvasGTK as FigureCanvas


class Graph(object):
    def __init__(self,tipo):
        self.cuento = 0
        self.magico = 800
        self.app = None
        self.tipo = tipo
        self.data = np.array([])
        self.fechas = np.array([])
        self.dpi = 100
        self.f = Figure((3.0, 3.0), dpi=self.dpi)
        self.f.subplots_adjust(hspace=1, left=.05, right = .99, top=.92   )
        self.a = self.f.add_subplot(111)
        self.a.set_axis_bgcolor('white')
        setp(self.a.get_xticklabels(), fontsize=8)
        setp(self.a.get_yticklabels(), fontsize=8)
        self.plot_data= self.a.plot(
            self.data, 
            linewidth= 1.4,
            color= tipo.color,
            )[0]
        self.plot_data2 = self.a.plot(
            np.array([]),
            linestyle= "--",
            linewidth= 1.4,
            color= "g",
            )[0]
        self.a.grid(True)
#        self.a.set_xlabel('Time')
        self.a.set_ylabel(tipo.formal)
        self.canvas = FigureCanvas(self.f)

    @inlineCallbacks    
    def on_redraw_timer(self):
        from twisted.internet import reactor
        self.tiempo = time.time()
        if not self.app.is_stoped:
            # if paused do not add data, but still redraw the plot
            # (to respond to scale modifications, grid change, etc.)
            #
            #print "They have called me!"
            numero = self.tipo.actual
            if numero:
                self.data = np.append (self.data, float(numero))# .append(float()) acá le agrega le dato 
                self.fechas = np.append(self.fechas, self.cuento)
                self.cuento += 1
                if self.fechas.size > self.magico:
                    self.data = np.delete(self.data, 0)
                    self.fechas = np.delete(self.fechas, 0)
                xmax = self.fechas.max() if self.fechas.max() > self.magico else self.magico
                xmin = xmax - self.magico
                #ymin = round(self.data.min(), 0) - 1
                ymin = -.5
                ymax = round(self.data.max(), 0) + 1
                self.a.set_xbound(lower=xmin, upper=xmax)
                self.a.set_ybound(lower=ymin, upper=ymax)
                self.plot_data2.set_xdata(np.array([0, xmax]))
                yield
                self.plot_data2.set_ydata(np.array([self.tipo.medio]*2))
            #self.fechas = np.append(self.fechas, datetime())
            yield
            setp(self.a.get_xticklabels(), 
                visible=True)
            yield
            #print np.arange(self.data.size) == self.fechas
            self.plot_data.set_xdata(self.fechas)
            yield
            self.plot_data.set_ydata(self.data)
            yield
            d = Deferred()
            reactor.callLater(.1, d.callback, None)
            yield d
            self.canvas.draw()
            yield
        else:
            d = Deferred()
            reactor.callLater(.1, d.callback, None)
            yield d
        reactor.callLater(time.time() - self.tiempo -.1, self.on_redraw_timer)
 
class Graphtemp(object):
    def __init__(self,tipo):
        self.cuento = 0
        self.magico = 800
        self.app = None
        self.tipo = tipo
        self.data = np.array([])
        self.fechas = np.array([])
        self.caldera = np.array([])
        self.dpi = 100
        self.f = Figure((3.0, 3.0), dpi=self.dpi)
        self.f.subplots_adjust(hspace=1, left=.05, right = .99, top=.92   )
        self.a = self.f.add_subplot(111)
        self.a.set_axis_bgcolor('white')
        setp(self.a.get_xticklabels(), fontsize=8)
        setp(self.a.get_yticklabels(), fontsize=8)
        self.plot_data= self.a.plot(
            self.data, 
            linewidth= 1.4,
            color= tipo.color,
            )[0]
        self.plot_data2 = self.a.plot(
            np.array([]),
            linestyle= "--",
            linewidth= 1.4,
            color= "g",
            )[0]
        self.plot_data3 = self.a.plot(
            np.array([]),
            linestyle= "--",
            linewidth= 1.4,
            color= "r",
            )[0]
        self.a.grid(True)
#        self.a.set_xlabel('Time')
        self.a.set_ylabel(tipo.formal)
        self.canvas = FigureCanvas(self.f)

    @inlineCallbacks    
    def on_redraw_timer(self):
        from twisted.internet import reactor
        self.tiempo = time.time()
        if not self.app.is_stoped:
            # if paused do not add data, but still redraw the plot
            # (to respond to scale modifications, grid change, etc.)
            #
            #print "They have called me!"
            numero = self.tipo.actual
            if numero:
                self.data = np.append (self.data, float(numero))# .append(float()) acá le agrega le dato 
                self.fechas = np.append(self.fechas, self.cuento)
                self.caldera = np.append(self.caldera, 40 if self.app.caldera.actual else 20)
                self.cuento += 1
                if self.fechas.size > self.magico:
                    self.data = np.delete(self.data, 0)
                    self.fechas = np.delete(self.fechas, 0)
                    self.caldera = np.delete(self.caldera, 0)
                xmax = self.fechas.max() if self.fechas.max() > self.magico else self.magico
                xmin = xmax - self.magico
                #ymin = round(self.data.min(), 0) - 1
                ymin = -.5
                ymax = 42#round(self.data.max(), 0) + 1
                self.a.set_xbound(lower=xmin, upper=xmax)
                self.a.set_ybound(lower=ymin, upper=ymax)
                self.plot_data2.set_xdata(np.array([0, xmax]))
                yield
                self.plot_data2.set_ydata(np.array([self.tipo.medio]*2))
            #self.fechas = np.append(self.fechas, datetime())
            yield
            setp(self.a.get_xticklabels(), 
                visible=True)
            yield
            #print np.arange(self.data.size) == self.fechas
            self.plot_data.set_xdata(self.fechas)
            self.plot_data.set_ydata(self.data)
            yield
            self.plot_data3.set_ydata(self.caldera)
            self.plot_data3.set_xdata(self.fechas)
            yield
            d = Deferred()
            reactor.callLater(.1, d.callback, None)
            yield d
            self.canvas.draw()
            yield
        else:
            d = Deferred()
            reactor.callLater(.1, d.callback, None)
            yield d
        reactor.callLater(time.time() - self.tiempo -.1, self.on_redraw_timer)

