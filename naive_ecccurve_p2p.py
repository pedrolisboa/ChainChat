import socket
import threading
import select
import sys
import time
import random
import binascii
from os import urandom
from eccsnacks.curve25519 import scalarmult, scalarmult_base

def main():

    def padKey(number):
        """Pad number adding extras 0 on the left"""
        temp = str(number)
        while len(temp) < 32:
            temp = '0' + temp
        return temp

    class Chat_Server(threading.Thread):
        """Server thread"""
        def __init__(self):
            threading.Thread.__init__(self)
            self.running = 1
            self.conn = None
            self.port = None
            self.addr = None

        def run(self):
            HOST = ''
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST,self.port))
            s.listen(1)
            self.conn, self.addr = s.accept()

            # Curve25519 encryption scheme
            # Usign a size-32 key
            a = urandom(32)
            a_pub = scalarmult_base(a)

            # send public key
            print(binascii.hexlify(a_pub))
            self.conn.send(a_pub)

            b_pub = self.conn.recv(32)
            secret = scalarmult(a, b_pub)

            print("Private Key A: " +binascii.hexlify(a))
            print("Public Key A: " +binascii.hexlify(a_pub))
            print("Public Key B: " +binascii.hexlify(b_pub))
            print("Shared key: " + binascii.hexlify(secret))


            # Select loop for listen
            while self.running == True:
            

        def kill(self):
            self.running = 0
     
    class Chat_Client(threading.Thread):
        """Client thread"""

        def __init__(self):
            threading.Thread.__init__(self)
            self.host = None
            self.sock = None
            self.port = None
            self.running = 1
        def run(self):              
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(5.0)
            try:
                self.sock.connect((self.host, self.port))
            except socket.timeout:
                print("Timeout, host inacessivel")
                connecter.config(state=NORMAL)
                raise SystemExit(0)

            print("Conectado ao peer:"+ self.host +
                    " on port: " + str(self.port))

            # Curve25519 encryption scheme
            # Usign a size-32 key
            a = urandom(32)
            a_pub = scalarmult_base(a)

            # send public key
            self.sock.send(a_pub)

            b_pub = self.sock.recv(32)

            secret = scalarmult(a, b_pub)

            print("Private Key A: " +binascii.hexlify(a))
            print("Public Key A: " +binascii.hexlify(a_pub))
            print("Public Key B: " +binascii.hexlify(b_pub))
            print("Shared key: " + binascii.hexlify(secret))
            
            # Select loop for listen
            while self.running == True:
            
        def kill(self):
            self.running = 0
            
    # Prompt, object instantiation, and threads start here.

    if not len(sys.argv) == 5:
        print("Listen: p2p.py <userid> <peerid> listen <port>")

        print("Connect: p2p.py <userid> <peerid> <peer_ip> <port>")

    my_ip = sys.argv[1]
    peer_ip = sys.argv[2]

    if sys.argv[3].lower() == 'listen':
        chat_server = Chat_Server()
        chat_client = Chat_Client()
        chat_server.port = int(sys.argv[4]) + i
        chat_server.start()
        
    else:
        chat_server = Chat_Server()
        chat_client = Chat_Client()
        chat_client.host = sys.argv[3]
        chat_client.port = int(sys.argv[4]) + i
        chat_client.start()
    

if __name__ == "__main__":
    main()

