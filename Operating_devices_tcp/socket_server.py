# socket_server.py

# Server Part
# Reference: https://lidron.tistory.com/44


"""
210624 file receiving function added @Young-hoon Ji

"""


import tqdm
import socketserver
import threading

HOST = ''
PORT = 
NUM_DEVICE = 0
lock = threading.Lock()

class UserManager:
    def __init__(self):
        self.users = {}

    def addUser(self, username, conn, addr):
        if username in self.users:
            conn.send('Already registered Device\n'.encode())
            return None

        lock.acquire()
        self.users[username] = (conn, addr)
        lock.release()

        self.sendMessageToAll('[%s] Connected to Server' %username)
       
        return username

    def messageHandler(self, username, msg):
        if msg[0] != '/':
            self.sendMessageToAll(msg)
            #print(msg)
            #print(username)
            if(msg=="file" or msg=="FILE"):
                self.receiveFile(msg)
            return

    def sendMessageToAll(self, msg):
        for conn, addr in self.users.values():
            conn.send(msg.encode())

    def receiveFile(self, msg): # 210624 added yhji
        print("Inside of function")
        for conn, addr in self.users.values():
            file = open("recv.txt", "wb") # recv file name to write

            RecvData = conn.recv(1024)
            while RecvData:
                print("Receiving")
                file.write(RecvData)
                RecvData = conn.recv(1024)
                
                if(RecvData==b"eof"):
                    break

            file.close()

        print("File Received")

        return
        


# class react when request comes from client
class TCPHandler(socketserver.BaseRequestHandler):
    userman = UserManager()
   
    def handle(self):
        print('[%s] Connected' %self.client_address[0])

        try:
            username = self.registerUsername()
            
            connected_devices = list(self.userman.users.keys())
            for device in connected_devices:
                print(device, end=", ")
            print("Num Devices Connected [%d / %d]" %(len(self.userman.users), NUM_DEVICE))

            if(len(self.userman.users) == NUM_DEVICE):
                print("All devices ready to be operated")
                while True:
                    msg = input("Type the command: ")
                    if(not msg):
                        ####### try to get input one more
                        print("Check the command provided")
                        while(msg):
                            msg = input("ReType the command: ")
                    elif(msg == "quit"):
                        print('===> Closing operating system.')
                        print('===> Type Ctrl+C to end the System.')
                        return
                    #print(msg)

                    # Handle 
                    self.userman.messageHandler(username, msg)
            else:
                msg = self.request.recv(1024)
        except Exception as e:
            print(e)

    def registerUsername(self):
        while True:
            #self.request.send('Device ID:'.encode())
            username = self.request.recv(1024)
            username = username.decode()
            if self.userman.addUser(username, self.request, self.client_address):
                return username

class OperatingServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass
       
def runServer():
    print('===> Start Device Operating System.')
    print('===> Type Ctrl+C to end the System.')

    try:
        socketserver.TCPServer.allow_reuse_address = True
        server = OperatingServer((HOST, PORT), TCPHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
        server.server_close()

    print("\n===> Server Shutting down")

if __name__=="__main__":
    NUM_DEVICE = int(input("Type num of Devices you operate: "))

    runServer()
