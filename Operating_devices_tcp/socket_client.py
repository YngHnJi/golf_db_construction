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

import utils.gears_macro as gears_macro
#import src.utils as utils

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

    def __init__(self, HOST, PORT, DEVICE_NAME, SAVE_ROOT):
        self.host_ip = HOST
        self.host_port = PORT
        self.device_name = DEVICE_NAME
        self.save_root = SAVE_ROOT
        
        # kinect variable
        self.kinect_toggle = 0

        #self.win_gears = gw.getWindowsWithTitle("Gears - Sports")[0]
        #self.win_kinect = gw.getWindowsWithTitle("KinectAzure.exe")[0]
        
        # gears variable
        self.gears_counter = 2
        self.save_dir = "C:\\Users\\GEARS\\Desktop\\GEARS_Data_PostProcess\\okay2del\\210629\\test4\\"

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
            self.logger.addHandler(file_handler)

    def conn2server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.host_ip, self.host_port))
            #print("Connecting to Server")
            self.logger.info("Connecting to Server")
            init_id = self.device_name
            sock.send(init_id.encode())

            self.rcvMsg(sock)

    def rcvMsg(self, sock):
        while True:
            try:
                data = sock.recv(1024)
                if not data or (data.decode() == "quit"):
                    #print("===> Client closed")
                    self.logger.info("===> Client closed")
                    break

                # Device Operating part
                #print("Received CMD: ", data.decode())
                cmd_string = "Received CMD: " + str(data.decode()) 
                self.logger.info(cmd_string)
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
                        self.logger.info("Not supported Device Name")
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
                self.logger.info("Start")
            else:
                self.logger.info("End")
            
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

        #print("Gears Connected")
        #self.win_gears.activate() # activate gears window to manage
        win_gears = gw.getWindowsWithTitle("Gears - Sports")[0]

        #print("Run GEARS")

        if(cmd=="SCAN"):
            # move mouse cursor to scan icon
            win_gears.activate()
            print("scan")
            pyautogui.moveTo(69, 1049)                # x 69 y 1049, for scan ball button
            pyautogui.click()       
        elif(cmd=="R"):
            win_gears.activate()
            pyautogui.moveTo(14, 1056)                # x 14, y 1056, for record button
            pyautogui.click()
            self.gears_counter += 1
        elif(cmd=="SAVE"):
            gears_macro.gears_save(self.save_dir, self.gears_counter) # 
            #self.gears_counter = 0
        elif(cmd=="DIR"):
            playername_data = socket.recv(1024)
            player_name = playername_data.decode()
            self.save_dir = self.save_root + "\\" + player_name + "\\"
            
            temp_str = "Save Dir : " + self.save_dir
            self.logger.info(temp_str)
        elif(cmd=="FILE"):
            self.sendFile(socket)


def runSys(DEVICE_NAME, SAVE_ROOT):
    HOST = 
    PORT = 
    client = socket_client(HOST, PORT, DEVICE_NAME, SAVE_ROOT)

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
            SAVE_ROOT = str(input("Typed File save root: "))

    file_handler = logging.FileHandler(filename=DEVICE_NAME+".log")

    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    runSys(DEVICE_NAME, SAVE_ROOT)