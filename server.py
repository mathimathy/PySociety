import socket
import threading
from crypto import rsa

class ThreadForClient(threading.Thread):
    def __init__(self, conn, address, id, publicKey, privateKey):
        threading.Thread.__init__(self)
        self.conn=conn
        self.address=address
        self.id=id
        self.rsa=rsa.RSA()
        self.rsa.private=privateKey
        key=self.receive().split(",")
        self.rsa.public=(int(key[0]),int(key[1]))
        print(f"Le client {self.id} vient de se connecter. Key: {self.rsa.public}")
        self.send(f"{publicKey[0]},{publicKey[1]}")

    def run(self):
        data = self.cryptedReceive()
        print(f"{self.id}: {data}")
        self.cryptedSend("Received")
    
    def cryptedSend(self, msg):
        msg=self.rsa.cipher(msg, self.rsa.private)
        self.send(str(msg))
    
    def cryptedReceive(self):
        msg = self.receive()
        data = hex(self.rsa.decipher(int(msg), self.rsa.public))[2:]
        data = "".join([chr(int("0x"+data[i:i+2],16)) for i in range(0,len(data),2)])
        return data
    
    def receive(self):
        data = self.conn.recv(1024)
        data = data.decode("utf8")
        return data
    
    def send(self, msg):
        msg = msg.encode('utf8')
        self.conn.sendall(msg)

class Server:
    def __init__(self, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.hp=('', port)
        self.rsa = rsa.RSA()
        self.rsa.createKey()
        self.clients=[]
    
    def loop(self):
        while True:
            self.socket.listen(5)
            conn, address = self.socket.accept()

            self.clients.append(ThreadForClient(conn,address, len(self.clients), self.rsa.public, self.rsa.private))
            self.clients[-1].start()
    
    def run(self):
        try:
            self.socket.bind(self.hp)
            print("Le serveur est démarré")
            self.loop()
        except Exception as e:
            print("Erreur: "+str(e))
        finally:
            self.socket.close()

if __name__=="__main__":
    server = Server(int(input("Port: ")))
    server.run()