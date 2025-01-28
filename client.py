import socket

class Client:
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.hp=(host,port)
    
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
            self.send(cmd)
            rec = self.receive()
            print(rec)
    
    def run(self):
        try:
            self.socket.connect(self.hp)
            self.loop()
        except Exception as e:
            print("Erreur"+str(e))
        finally:
            self.socket.close()

if __name__=="__main__":
    client = Client(input("Host: "), int(input("Port: ")))
    client.run()