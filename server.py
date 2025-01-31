import socket
import threading
from crypto import rsa,sign
from serverScript import receive
import sqlite3

class ThreadForClient(threading.Thread):
    def __init__(self, conn, address, id, publicKey, privateKey, spbk, sprk):
        threading.Thread.__init__(self)
        self.listid=id
        self.working=True
        self.conn=conn
        self.address=address
        self.rsa=rsa.RSA()
        self.rsa.private=privateKey
        self.publicKey = publicKey
        self.spbk = spbk
        self.sprk = sprk
    
    def loop(self):
        while self.working:
            data = self.cryptedReceive()
            print(f"{self.id}: {data}")
            receive.receive(self, data)
    
    def quit(self):
        self.working=False

    def run(self):
        try:
            self.db = sqlite3.connect("server.db")
            self.cursor = self.db.cursor()
            account=self.receive()
            print(account)
            if account=="1":
                self.send("ok")
                data=self.receive().split(",")
                print(data)
                self.cursor.execute(f"SELECT * FROM users WHERE username='{data[0]}' and pwd={int(data[1])}")
                user = self.cursor.fetchone()
                print(user)
                if user==None:
                    self.send("0")
                else:
                    self.id=user[0]
                    self.firstname=user[1]
                    self.lastname=user[2]
                    self.username=user[3]
                    key = user[4].split(",")
                    self.rsa.public=(int(key[0]),int(key[1]))
                    skey=user[5].split(",")
                    self.sign = sign.Sign(False, (int(skey[0]),int(skey[1])), self.sprk)
                    self.pwd=int(user[6])
                    self.cursor.execute(f"SELECT * FROM bank WHERE id={self.id}")
                    self.amount=self.cursor.fetchone()[1]
                    self.send("1")
            else:
                print("ok")
                self.send("ok")
                #self.id=id
                key=self.receive().split(",")
                self.send("ok")
                print(key)
                self.rsa.public=(int(key[0]),int(key[1]))
                skey = self.receive().split(",")
                self.send("ok")
                print(skey)
                self.sign = sign.Sign(False, (int(skey[0]),int(skey[1])), self.sprk)
                data = self.receive().split(",")
                print(data)
                self.firstname=data[0]
                self.lastname=data[1]
                self.username=data[2]
                self.amount=0
                self.pwd=int(data[3])
                self.db.execute(f'INSERT INTO users (firstname,surname,username,rsaKey,signKey,pwd) VALUES ("{self.firstname}","{self.lastname}","{self.username}","{self.rsa.public[0]},{self.rsa.public[1]}","{self.sign.rsa.public[0]},{self.sign.rsa.public[1]}",{self.pwd})')
                self.db.execute('INSERT INTO bank (amount) VALUES (0)')
                self.db.commit()
                self.cursor.execute(f"SELECT * FROM users WHERE username='{self.username}' and pwd={self.pwd}")
                self.id=self.cursor.fetchone()[0]
            print(f"Le client {self.id} vient de se connecter.")
            self.send(f"{self.publicKey[0]},{self.publicKey[1]}")
            self.receive()
            self.send(f"{self.spbk[0]},{self.spbk[1]}")
            self.loop()
        except Exception as e:
            print(f"{self.id} raised an exception: {e}")
        finally:
            self.conn.close()
            self.db.close()
    
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
    
    def receive(self):
        data = self.conn.recv(4096)
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
        self.sign = sign.Sign()
        self.clients=[]
    
    def loop(self):
        while True:
            self.socket.listen(5)
            conn, address = self.socket.accept()
            for index in range(len(self.clients)):
                if self.clients[index].working==False:
                    del self.clients[index]
            self.clients.append(ThreadForClient(conn,address, len(self.clients), self.rsa.public, self.rsa.private, self.sign.rsa.public, self.sign.rsa.private))
            self.clients[-1].start()
    
    def run(self):
        try:
            self.socket.bind(self.hp)
            print("Le serveur est démarré")
            self.loop()
        except Exception as e:
            print("Erreur: "+str(e))
        finally:
            self.db.close()
            self.socket.close()

if __name__=="__main__":
    server = Server(int(input("Port: ")))
    server.run()