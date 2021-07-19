#!/usr/bin/python3
# -*- coding: utf-8 -*-

#CIFRADO CESAR
__author__ = "arielbalo"

import argparse
from components import server, client

BANNER = """
                                 ____
                                /.   \ 
       .  ,                    |___   |
      (\;/)                 _______|  |
     oo   \//,        _    /          | |\ 
   ,/_;~      \,     / '  |   _______/  | \ 
  "'    (  (   \    !     |  |   _______|  |
       //  \   |__.'       \ |  /          |
      '~  '~----''          \| |   _______/
                               |  |___
                               |    . |
                                \____/
  ____       _     ____              _          
 |  _ \ __ _| |_  / ___| _ __   __ _| | _____   
 | |_) / _` | __| \___ \| '_ \ / _` | |/ / _ \  
 |  _ < (_| | |_   ___) | | | | (_| |   <  __/  
 |_| \_\__,_|\__| |____/|_| |_|\__,_|_|\_\___|
"""

def parse_args():
    parser = argparse.ArgumentParser(description="RatSnake.",
                                     epilog="Más información en https://github.com/arielbalo/RatSnake/")
    parser.add_argument("-c", "--client", action="store_true", help="Modo Cliente")
    parser.add_argument("-s", "--server", action="store_true", help="Modo Servidor")
    parser.add_argument("-p", "--port", type=int, default=1337, help="Puerto a emplear")
    args = parser.parse_args()
    return args

def main(args):
    print(BANNER)
    port = args.port

    if args.client:
        servicio = client.Clientes(port)
    elif args.server:
        servicio = server.Servidor(port)
        servicio.setDaemon(True)
        servicio.start()
        servicio.runShell()
        
    else:
        print("\nRevise el panel de ayuda [-h]\n")

if __name__ == '__main__':
    args = parse_args()
    main(args)