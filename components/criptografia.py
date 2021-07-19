from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA3_256


pad = lambda s: s + b'\0' * (AES.block_size - len(s) % AES.block_size)
clave = 'Una clave muy muy dificil.'.encode('utf-8')

def cifrar(textoclaro, key):
    textoclaro = pad(textoclaro)
    iv = Random.new().read(AES.block_size)
    cifrador = AES.new(key, AES.MODE_CFB, iv)
    return iv + cifrador.encrypt(textoclaro)

def descifrar(textocifrado, key):
    iv = textocifrado[:AES.block_size]
    descifrador = AES.new(key, AES.MODE_CFB, iv)
    return descifrador.decrypt(textocifrado[AES.block_size:]).rstrip(b'\0')

def gen_key():
    return SHA3_256.new(clave).digest()