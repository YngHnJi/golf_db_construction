# socket_client.py

# Client Part
# Reference: https://lidron.tistory.com/44

import socket
import ntplib
from threading import Thread
from time import ctime

import pyautogui
import pygetwindow as gw

class sync_time(): # class to sync time based on provided domain 
    def __init__(self, ntp_domain):
        self.timeServer = ntp_domain # "time.windows.com"
        self.c = ntplib.NTPClient()
    
    def get_NTPTime(self):
        response = self.c.request(self.timeServer, version=3)
        cur_time = ctime(response.tx_time)
        print("diff b/w Sever and Local time %.2f s" %(response.offset))

        return cur_time

class socket_client():
    time_sync = sync_time("time.windows.com")

    def __init__(self, HOST, PORT, DEVICE_NAME):
        self.host_ip = HOST
        self.host_port = PORT
        self.device_name = DEVICE_NAME

    def conn2server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.host_ip, self.host_port))
            print("Connecting to Server")
            init_id = self.device_name
            sock.send(init_id.encode())

            self.rcvMsg(sock)

    def rcvMsg(self, sock):
        while True:
            try:
                data = sock.recv(1024)
                if not data or (data.decode() == "quit"):
                    print("===> Client closed")
                    break

                # Device Operating part
                print("Received CMD: ", data.decode())
                if(data.decode() == "time"):
                    print(self.time_sync.get_NTPTime())
                else:
                    if(self.device_name=="GEARS"):
                        print("Run GEARS")
                    elif(self.device_name=="KINECT"):
                        #print("Run Kinect")
                        self.runKinect(data)
                    else:
                        print("Not supported Device name")
            except:
                pass

    def runKinect(self, rcv_data):
        cmd = rcv_data.decode()
        win = gw.getWindowsWithTitle("KinectAzure.exe")[0]
        
        if(cmd == "V" or cmd == "v"):
            #print("Show")
            pyautogui.press("v")
        elif(cmd == "R" or cmd == "r"):
            #print("Record")
            pyautogui.press("r")
        elif(cmd == "Q" or cmd == "q"):
            #print("Quit")
            pyautogui.press("q")
        elif(cmd == "esc"):
            #print("esc")
            pyautogui.press("esc")
        else: # i don't think it's essential to write code for extract and set dir
            pass

def runSys(DEVICE_NAME):
    #HOST = "localhost"
    client = socket_client(HOST, PORT, DEVICE_NAME)

    client.conn2server()

if __name__=="__main__":
    DEVICE_NAME = None

    if(DEVICE_NAME==None):
        name_flag = False
        bool_name = None

        while(name_flag==False):
            DEVICE_NAME = str(input("Type the name of Device to operate by server(GEARS, KINECT): "))
            bool_name = str(input("Typed Device is {}, is it right? Type (y/n) and enter : ".format(DEVICE_NAME)))
            if(bool_name=="y"):
                name_flag = True
    runSys(DEVICE_NAME)