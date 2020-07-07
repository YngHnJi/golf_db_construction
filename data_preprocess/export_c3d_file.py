# print_c3d_file.py

import os
import c3d
import csv
import warnings
from tqdm import tqdm
import numpy as np
import pandas as pd

"""
"Marker_0:0:0", "WaistLeft", "WaistRight", "WaistLBack", "WaistRBack", "BackTop", "BackLeft", "BackRight", "HeadTop", "HeadFront", "HeadSide", "LShoulderTop", "LShoulderBack", "LElbowOut", "LUArmHigh", "LWristTop", "RShoulderTop", "RShoulderBack", "RElbowOut", "RUArmHigh", "RWristTop", "LKneeOut", "LToeIn", "LToeOut", "LAnkleOut", "RKneeOut", "RToeIn", "RToeOut", "RAnkleOut", "Marker_2:2:1","Marker_2:2:2", "Marker_2:2:3", "Marker_3:3:1", "Marker_3:3:2", "Marker_3:3:3", "Marker_3:3:4"
"""

warnings.filterwarnings("ignore")


def write_C3D2CSV(file_path:str, output_dir:str, print_flag=False):
    try:
        file_c3d = open(file_path, 'rb')
        file_csv = open(output_dir+"jointinfo.csv", "w", newline="")
    except IOError as e:
        print("Couldn't open or write to file (%s)." % e)

    reader = c3d.Reader(file_c3d)
    write_csv = csv.writer(file_csv)
    
    write_csv.writerow(["Frame", "Marker_0:0:0 X", "Marker_0:0:0 Y", "Marker_0:0:0 Z", 
                        "WaistLeft X", "WaistLeft Y", "WaistLeft Z", 
                        "WaistRight X", "WaistRight Y", "WaistRight Z", 
                        "WaistLBack X", "WaistLBack Y", "WaistLBack Z", 
                        "WaistRBack X", "WaistRBack Y", "WaistRBack Z", 
                        "BackTop X", "BackTop Y", "BackTop Z", 
                        "BackLeft X", "BackLeft Y", "BackLeft Z", 
                        "BackRight X", "BackRight Y", "BackRight Z", 
                        "HeadTop X", "HeadTop Y", "HeadTop Z", 
                        "HeadFront X", "HeadFront Y", "HeadFront Z", 
                        "HeadSide X", "HeadSide Y", "HeadSide Z", 
                        "LShoulderTop X", "LShoulderTop Y", "LShoulderTop Z", 
                        "LShoulderBack X", "LShoulderBack Y", "LShoulderBack Z", 
                        "LElbowOut X", "LElbowOut Y", "LElbowOut Z", 
                        "LUArmHigh X", "LUArmHigh Y", "LUArmHigh Z", 
                        "LWristTop X", "LWristTop Y", "LWristTop Z",
                        "RShoulderTop X", "RShoulderTop Y", "RShoulderTop Z", 
                        "RShoulderBack X", "RShoulderBack Y", "RShoulderBack Z", 
                        "RElbowOut X", "RElbowOut Y", "RElbowOut Z", 
                        "RUArmHigh X", "RUArmHigh Y", "RUArmHigh Z", 
                        "RWristTop X", "RWristTop Y", "RWristTop Z", 
                        "LKneeOut X", "LKneeOut Y", "LKneeOut Z", 
                        "LToeIn X", "LToeIn Y", "LToeIn Z", 
                        "LToeOut X", "LToeOut Y", "LToeOut Z", 
                        "LAnkleOut X", "LAnkleOut Y", "LAnkleOut Z", 
                        "RKneeOut X", "RKneeOut Y", "RKneeOut Z", 
                        "RToeIn X", "RToeIn Y", "RToeIn Z", 
                        "RToeOut X", "RToeOut Y", "RToeOut Z", 
                        "RAnkleOut X", "RAnkleOut Y", "RAnkleOut Z", 
                        "Marker_2:2:1 X", "Marker_2:2:1 Y","Marker_2:2:1 Z",
                        "Marker_2:2:2 X", "Marker_2:2:2 Y", "Marker_2:2:2 Z", 
                        "Marker_2:2:3 X", "Marker_2:2:3 Y", "Marker_2:2:3 Z", 
                        "Marker_3:3:1 X", "Marker_3:3:1 Y", "Marker_3:3:1 Z", 
                        "Marker_3:3:2 X", "Marker_3:3:2 Y", "Marker_3:3:2 Z", 
                        "Marker_3:3:3 X", "Marker_3:3:3 Y", "Marker_3:3:3 Z", 
                        "Marker_3:3:4 X", "Marker_3:3:4 Y", "Marker_3:3:4 Z"])

    for i, points, analog in tqdm(reader.read_frames()):
        if(print_flag==True):    
            print("====> Frame Num: ", i)
            for j in range(points.shape[0]):
                print(points[j])

        write_csv.writerow([i, points[0][0], points[0][1], points[0][2],
                            points[1][0], points[1][1], points[1][2],
                            points[2][0], points[2][1], points[2][2],
                            points[3][0], points[3][1], points[3][2],
                            points[4][0], points[4][1], points[4][2],
                            points[5][0], points[5][1], points[5][2],
                            points[6][0], points[6][1], points[6][2],
                            points[7][0], points[7][1], points[7][2],
                            points[8][0], points[8][1], points[8][2],
                            points[9][0], points[9][1], points[9][2],
                            points[10][0], points[10][1], points[10][2],
                            points[11][0], points[11][1], points[11][2],
                            points[12][0], points[12][1], points[12][2],
                            points[13][0], points[13][1], points[13][2],
                            points[14][0], points[14][1], points[14][2],
                            points[15][0], points[15][1], points[15][2],
                            points[16][0], points[16][1], points[16][2],
                            points[17][0], points[17][1], points[17][2],
                            points[18][0], points[18][1], points[18][2],
                            points[19][0], points[19][1], points[19][2],
                            points[20][0], points[20][1], points[20][2],
                            points[21][0], points[21][1], points[21][2],
                            points[22][0], points[22][1], points[22][2],
                            points[23][0], points[23][1], points[23][2],
                            points[24][0], points[24][1], points[24][2],
                            points[25][0], points[25][1], points[25][2],
                            points[26][0], points[26][1], points[26][2],
                            points[27][0], points[27][1], points[27][2],
                            points[28][0], points[28][1], points[28][2],
                            points[29][0], points[29][1], points[29][2],
                            points[30][0], points[30][1], points[30][2],
                            points[31][0], points[31][1], points[31][2],
                            points[32][0], points[32][1], points[32][2],
                            points[33][0], points[33][1], points[33][2],
                            points[34][0], points[34][1], points[34][2],
                            points[35][0], points[35][1], points[35][2],
        ])

    file_csv.close()

    print("Data Export .C3D to .CSV done")

def print_c3d(file_path):
    reader = c3d.Reader(open(file_path, 'rb'))
    
    for i, points, analog in reader.read_frames():
        print("====> Frame Num: ", i)
        for j in range(points.shape[0]):
            print(points[j])


if __name__=="__main__":
    file_path = "/Users/younghoonji/Desktop/2020_Spring/Project/golf_db/gears_data/200514/C3DExport.c3d"
    output_dir = "/Users/younghoonji/Desktop/2020_Spring/Project/golf_db/gears_data/200514/"

    write_C3D2CSV(file_path, output_dir) # input_file extension .c3d

    file_pandas = "/Users/younghoonji/Desktop/2020_Spring/Project/golf_db/gears_data/200514/"

    file_pandas = "/Users/younghoonji/Desktop/2020_Spring/Project/golf_db/gears_data/200512/jointinfo.csv"
    timestamp_pandas = ""
    add_timestamp()
    
