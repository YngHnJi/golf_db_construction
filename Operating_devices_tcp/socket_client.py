# socket_client.py

# Client Part
# Reference: https://lidron.tistory.com/44
# file transfer : https://github.com/linuxhintcode/websamples/blob/master/python_send_file/server.py

"""
log

210624 file tranfer module added @ Young-hoon Ji
https://github.com/linuxhintcode/websamples/blob/master/python_send_file/server.py

"""


import os
import socket
import ntplib
from threading import Thread
from time import ctime
import logging

import pyautogui
import pygetwindow as gw

import src.utils as utils

logger = logging.getLogger("KinectAzure")
logger.setLevel(logging.INFO)
formatter = logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(message)s")

stream_handler = logging.StreamHandler()
file_handler = None

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
        self.kinect_toggle = 0

        self.logdir= ".\\log"
        if((os.path.exists(self.logdir)) != True):
            os.mkdir(self.logdir) # if log fir not exists, make one

        self.logger = logging.getLogger(DEVICE_NAME)

    def initLogger(self, stream_log=True, file_log=True):
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(message)s")

        stream_handler = None
        file_handler = None

        if(stream_log == True):
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            self.logger.addHandler(stream_handler)
        if(file_log == True):
            file_handler = logging.FileHandler(filename=self.logdir+"\\"+self.device_name+".log")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

    def conn2server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.host_ip, self.host_port))
            #print("Connecting to Server")
            logger.info("Connecting to Server")
            init_id = self.device_name
            sock.send(init_id.encode())

            self.rcvMsg(sock)

    def rcvMsg(self, sock):
        while True:
            try:
                data = sock.recv(1024)
                if not data or (data.decode() == "quit"):
                    #print("===> Client closed")
                    logger.info("===> Client closed")
                    break

                # Device Operating part
                #print("Received CMD: ", data.decode())
                cmd_string = "Received CMD: " + str(data.decode()) 
                logger.info(cmd_string)
                if(data.decode() == "time"):
                    print(self.time_sync.get_NTPTime())
                else:
                    if(self.device_name=="GEARS"):
                        self.runGears(data, sock)
                    elif(self.device_name=="KINECT"):
                        #print("Run Kinect")
                        self.runKinect(data, sock)
                    else:
                        #print("Not supported Device name")
                        logger.info("Not supported Device Name")
            except:
                pass

    def sendFile(self, sock):
        #print("File Transfer")
        file = open("sampledata.txt", "rb")

        SendData = file.read(1024)
        while SendData:
            print("Sending...")
            sock.send(SendData)
            SendData = file.read(1024)
            if(SendData==b""):
                sock.send(b"eof")
        
        return

    def runKinect(self, rcv_data, socket):
        cmd = rcv_data.decode()
        #win = gw.getWindowsWithTitle("KinectAzure.exe")[0]
        
        if(cmd == "V" or cmd == "v"):
            #print("Show")
            pyautogui.press("v")
        elif(cmd == "R" or cmd == "r"):
            #print("Record")
            if(self.kinect_toggle == 0):
                logger.info("Start")
            else:
                logger.info("End")
            
            self.kinect_toggle ^= 1 # toggle switch
            pyautogui.press("r")
        elif(cmd == "Q" or cmd == "q"):
            #print("Quit")
            pyautogui.press("q")
        elif(cmd == "esc"):
            #print("esc")
            pyautogui.press("esc")
        else: # i don't think it's essential to write code for extract and set dir
            pass

    def runGears(self, rcv_data, socket):
        cmd = rcv_data.decode()
        cmd = cmd.upper()

        print("Gears Connected")
        if(cmd=="FILE" or cmd=="file"):
            self.sendFile(socket)

        # use pyautogui.hotkey properly to make it.

def runSys(DEVICE_NAME):
    #HOST = "localhost"
    HOST = ""
    PORT = 
    client = socket_client(HOST, PORT, DEVICE_NAME)

    client.initLogger(stream_log=True, file_log=True)
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

    file_handler = logging.FileHandler(filename=DEVICE_NAME+".log")

    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    runSys(DEVICE_NAME)