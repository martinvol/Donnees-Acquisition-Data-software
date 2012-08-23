import poplib
from email.Parser import Parser

"""Encargado de revisar los mails y encontrar los comandos"""

class lector_email():
    """Clase utilizada para leer los emails de comandos"""
    def __init__(self, usuario, clave):
        """Se establece conexion con el servidor pop de gmail"""
        self.usuario = usuario
        self.clave = clave
        self.conectar()
        self.codigos = []
        self.codigos.append("ok")       #Definimos un codigo inicial y basico


    def conectar(self):
        """Se conecta con el servidor pop3"""
        self.m = poplib.POP3_SSL('pop.gmail.com',995)
        self.m.user(self.usuario)
        self.m.pass_(self.clave)
        print "conectado al server pop3"


    def definir_mensaje(self, nuevo_mensaje):
        """Agrega nuevo_mensaje a la lista sef.codigo"""
        self.codigos.append (nuevo_mensaje.lower())

    def cerrar_conexion(self):
        """Encargado de cerrar la coneccion"""
        self.m.quit()

    def actualizar(self):
        """Ontiene los datos del servidor"""
        print "llamada a actualizar"
        # Se obtiene el numero de mensajes pendientes y se hace un
        # bucle para cada mensaje
        self.numero = len(self.m.list()[1])
        for i in range (self.numero):
        #    print "Mensaje numero"+str(i+1)
        #    print "--------------------"
            # Se lee el mensaje
            self.response, self.headerLines, self.bytes = self.m.retr(i+1)
            # Se mete todo el mensaje en un unico string
            self.mensaje='\n'.join(self.headerLines)
            # Se parsea el mensaje
            self.p = Parser()
            self.email = self.p.parsestr(self.mensaje)
        # Se sacan por pantalla los campos from, to y subject
            print "From: "+self.email["From"]
            print "To: "+self.email["To"]
            print "Subject: "+self.email["Subject"]
            print self.email.get_content_type()
            print self.email.get_payload(decode=True)
            print self.email.is_multipart()
            self.tipo = self.email.get_content_type()
            for codigo in self.codigos:
                if ("text/plain" == self.tipo) and (self.email.get_payload(decode=True).lower() == codigo):
                # Si es texto plano, se escribe en pantalla
                    print self.email.get_payload(decode=True)
                    self.m.dele(i+1)             #le sumamos 1 ya que python cuenta desde 0 y los emails desde 1
                    self.cerrar_conexion()       #nos desconectamos solo si borramos algo, y lo borramos solo si es un mensaje de "ok"
                    self.conectar()              #y de esta forma se guardan los archivos en el server
                    return codigo                #retorna el comando que se encontro en el e-mail
        return False                    #retorna falso en caso de no encontrar nada


if __name__ == '__main__':
    #Esto es un test
    #    u = raw_input("introducir usuario gmail:")
    #    c = raw_input("introducir clave de la cuenta:")
    lec = lector_email("proyectotilapia2010@gmail.com", "pasopaso")
    print lec.actualizar()
    lec.cerrar_conexion()
