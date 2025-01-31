import socket
from crypto import rsa,sign,hash
from clientScript import receive
import getpass

class Client:
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.hp=(host,port)
        self.working=True
        self.rsa = rsa.RSA()
        self.rsa.createKey()
        self.sign=sign.Sign()
    
    def cryptedSend(self, msg):
        signature = self.sign.sign(msg)
        msg=self.rsa.cipher(msg, self.rsa.public)
        self.send(hex(signature)+","+str(msg))
    
    def cryptedReceive(self):
        msg = self.receive().split(",")
        signature = int(msg[0],16)
        msg = msg[1]
        data = hex(self.rsa.decipher(int(msg), self.rsa.private))[2:]
        data = "".join([chr(int("0x"+data[i:i+2],16)) for i in range(0,len(data),2)])
        if self.sign.checkSign(data,signature):
            return data

    def quit(self):
        self.working=False
    
    def send(self, data):
        data = data.encode("utf8")
        self.socket.sendall(data)
    
    def receive(self):
        reception = self.socket.recv(4096)
        reception = reception.decode("utf8")
        return reception
    
    def loop(self):
        while self.working:
            self.cmd = input("> ")
            self.cryptedSend(self.cmd)
            rec = self.cryptedReceive()
            receive.receive(self, rec)
    
    def run(self):
        try:
            self.socket.connect(self.hp)
            if input("As-tu un compte ? (oui,Non)")=="oui":
                self.send("1")
                self.receive()
                username = input("Quel est ton nom d'utilisateur ? ")
                pwd = hash.sha256(getpass.getpass("Quel est ton mot de passe ?"))
                self.send(f"{username},{pwd}")
                if self.receive()=="0":
                    print("Mauvais identifiants")
                    self.socket.close()
                    quit()
                with open("key.key") as f:
                    d = f.read().split('\n')
                    privateKey = d[0].split(",")
                    signPrivateKey = d[1].split(",")
                    self.rsa.private = (int(privateKey[0]),int(privateKey[1]))
                    self.sign.rsa.private = (int(signPrivateKey[0]),int(signPrivateKey[1]))
            else:
                print("Coucou")
                self.send("0")
                self.receive()
                self.send(f"{self.rsa.public[0]},{self.rsa.public[1]}")
                self.receive()
                self.send(f"{self.sign.rsa.public[0]},{self.sign.rsa.public[1]}")
                self.receive()
                firstname=input("Quel est ton prénom ? ")
                lastname=input("Quel est ton nom de famille ? ")
                surname=input("Quel est ton nom d'utilisateur ? ")
                pwd = hash.sha256(getpass.getpass("Quel est ton mot de passe ? "))
                self.send(f"{firstname},{lastname},{surname},{pwd}")
                with open("key.key", "w+") as f:
                    f.write(f"{self.rsa.private[0]},{self.rsa.private[1]}\n{self.sign.rsa.private[0]},{self.sign.rsa.private[1]}")
            key=self.receive().split(",")
            self.send("ok")
            self.rsa.public=(int(key[0]),int(key[1]))
            skey=self.receive().split(",")
            self.sign.rsa.public=(int(skey[0]),int(skey[1]))    
            self.loop()
        except Exception as e:
            print("Erreur: "+str(e))
        finally:
            self.socket.close()

if __name__=="__main__":
    client = Client(input("Host: "), int(input("Port: ")))
    client.run()