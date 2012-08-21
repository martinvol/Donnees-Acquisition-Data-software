from random import randint, choice
import time

class DataGen(object):
    """ A silly class that generates pseudo-random data for
        display in the plot.
    """
    def __init__(self, init=50):
        self.data = self.init = init
        
    def next(self):
        self._recalc_data()
        return self.data
    
    def _recalc_data(self):
        delta = random.uniform(-0.5, 0.5)
        r = random.random()

        if r > 0.9:
            self.data += delta * 15
        elif r > 0.8: 
            # attraction to the initial value
            delta += (0.5 if self.init > self.data else -0.5)
            self.data += delta
        else:
            self.data += delta


class Serial(object):
    def __init__(self, *args, **kargs):
        self.bool = True
        self.opciones = [-.1 ,.1] + [0]*3
        self.ph, self.temp, self.o2 = 75, 315, 50
        self.todos = (self.ph, self.temp, self.o2)
        self.counte = 0
        
    def readline(self):
        if self.bool:
            time.sleep(0.066666667)
            self.ph += choice(self.opciones)
            self.o2 += choice(self.opciones)
            self.temp += choice(self.opciones)
            #print "%03d%03d%03d\n" % (self.ph, self.o2, self.temp)
            _return =  "%03d%03d%03d\n" % (self.ph, self.o2, self.temp)
        else:
            self.counte = self.counte + 1
            if self.counte > 1000:
                self.counte = 0
                _return = "d\n"
            elif self.counte <= 500:
                _return = "e\n"
            elif self.counte > 500:
                _return = "d\n"
            #print _return

        self.bool = not self.bool
        return _return
           

    def flushInput(self):
        pass
