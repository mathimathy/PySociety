import socket
from crypto import rsa

class Client:
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.hp=(host,port)
        self.rsa = rsa.RSA()
        self.rsa.createKey()
    
    def cryptedSend(self, msg):
        msg=self.rsa.cipher(msg, self.rsa.private)
        self.send(str(msg))
    
    def cryptedReceive(self):
        msg = self.receive()
        data = hex(self.rsa.decipher(int(msg), self.rsa.public))[2:]
        data = "".join([chr(int("0x"+data[i:i+2],16)) for i in range(0,len(data),2)])
        return data

    
    def send(self, data):
        data = data.encode("utf8")
        self.socket.sendall(data)
    
    def receive(self):
        reception = self.socket.recv(1024)
        reception = reception.decode("utf8")
        return reception
    
    def loop(self):
        while True:
            cmd = input("> ")
            self.cryptedSend(cmd)
            rec = self.cryptedReceive()
            print(rec)
    
    def run(self):
        try:
            self.socket.connect(self.hp)
            self.send(f"{self.rsa.public[0]},{self.rsa.public[1]}")
            key=self.receive().split(",")
            self.rsa.public=(int(key[0]),int(key[1]))
            print(self.rsa.public)
            self.loop()
        except Exception as e:
            print("Erreur"+str(e))
        finally:
            self.socket.close()

if __name__=="__main__":
    client = Client(input("Host: "), int(input("Port: ")))
    client.run()