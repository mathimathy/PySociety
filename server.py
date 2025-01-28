import socket
import threading

class ThreadForClient(threading.Thread):
    def __init__(self, conn, address, id):
        threading.Thread.__init__(self)
        self.conn=conn
        self.address=address
        self.id=id
        print(f"Le client {self.id} vient de se connecter")
    
    def run(self):
        data = self.receive()
        print(f"{self.id}: {data}")
        self.send("Received")
    
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
        self.clients=[]
    
    def loop(self):
        while True:
            self.socket.listen(5)
            conn, address = self.socket.accept()

            self.clients.append(ThreadForClient(conn,address, len(self.clients)))
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