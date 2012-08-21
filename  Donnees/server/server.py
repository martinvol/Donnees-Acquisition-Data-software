from twisted.internet.protocol import  Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
import time

class ChatProtocol(LineReceiver):
    def lineReceived(self, line):
        print line
#        self.sendLine(line)
        self.factory.Id += 1
        self.sendLine(str(self.factory.Id))

    def connectionMade(self):
        self.factory.connections.append(self)
        for i in self.factory.app.lista_de_valores:
            enviar = getattr(self.factory.app, i["nombre"])
            actual = enviar.actual
            if actual and type(actual) is str:
                print enviar.actual
                self.sendLine(i["nombre"] + " " + enviar.actual + " " + enviar.tiempo.strftime("%H:%M:%S_%d/%m/%y"))
                #probar con el equipo, conectar sin prototipo

        print "Connection Made" 

    def connectionLost(self, reason):
        print "Conneciton Lost"
        self.factory.connections.remove(self)

class ChatFactory(Factory):
    Id = 0
    connections = []
    protocol = ChatProtocol
    app = None

    def sendConnected(self, valor, nombre, tiempo):
        for i in self.connections:
            i.sendLine(nombre + " " + valor + " " + tiempo)


def main():
    reactor.listenTCP(7777, factory)
    reactor.run()
    pass

if __name__ == '__main__':
    main()
