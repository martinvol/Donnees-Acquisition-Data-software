# -*- encoding: utf-8 -*-
#!/usr/bin/python


import serial
from sys import argv

if "-f" in argv:
    import serial_fake as serial
    print "fake"
else:
    import serial
    print "Puerto"

def is_int(a):
    """Si a es un entero, devuelve True"""
    try:
        int (a)
        return True
    except:
        return False

class Serial_(serial.Serial):
    counter = 0
    _buffer = ''

    def mis_datos(self):
        raw = self.readline()
        _return = dict()
        if len(raw) == 10 and is_int(raw):
            _return["ph"] = raw[:2] + "." + raw[2]
            _return["o2"] = raw[3:5] + "." + raw[5]
            _return["temp"] = raw[6:8]+ "." + raw[8]
#            print _return
            return _return
            
        elif raw == '':
            #aca van los scada
            #print raw, raw
            return None
        elif len(raw) == 2:
            raw = raw[0]
            self.counter += 1 
            if not raw in self._buffer:
                self._buffer += raw
            if self.counter > 5:
                self.counter = 0
                _return = dict()
                #print self._buffer
                if "e" in self._buffer:
                    #print self._buffer
                    _return["caldera"] = True
                    self._buffer = self._buffer.replace("e", "")
                else:
                    _return["caldera"] = False
                #print self._buffer
                if not "j" in self._buffer:
                    self._buffer += "n"
                if not "c" in self._buffer:
                    self._buffer += "z"
                _return["SCADA"] = self._buffer #DESTILDAR ESTO
                #_return["SCADA"] = "cja"
#                print self._buffer
                self._buffer = ''
                #print _return
                #print "retorne"
                return _return
            return dict()
        return dict()
