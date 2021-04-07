# post_process_GEARS.py

# This is a file to do preprocess for GEARS output files
# Young-hoon Ji, 210406

import os
import c3d
import csv
import warnings
from tqdm import tqdm
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

# data coordinated information
""" 
"Marker_0:0:0", "WaistLeft", "WaistRight", "WaistLBack", "WaistRBack", 
"BackTop", "BackLeft", "BackRight", "HeadTop", "HeadFront", "HeadSide", 
"LShoulderTop", "LShoulderBack", "LElbowOut", "LUArmHigh", "LWristTop", 
"RShoulderTop", "RShoulderBack", "RElbowOut", "RUArmHigh", "RWristTop", 
"LKneeOut", "LToeIn", "LToeOut", "LAnkleOut", "RKneeOut", "RToeIn", "RToeOut", "RAnkleOut", 
"Marker_2:2:1","Marker_2:2:2", "Marker_2:2:3", 
"Marker_3:3:1", "Marker_3:3:2", "Marker_3:3:3", "Marker_3:3:4"
"""


class GearsPostProcess():
    def __init__(self, _root_path:str, _save_path:str):
        self.root_path = _root_path
        self.save_path = _save_path

    def write_C3D2CSV(self, c3d_file_path:str, output_filename:str, print_flag=False):
        try:
            file_c3d = open(self.root_path + c3d_file_path, 'rb')
            file_csv = open(self.save_path + output_filename, "w", newline="")
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

    def write_C3D2DF(self, c3d_file_path:str): # export c3d file into pandas dataframe
        try:
            file_c3d = open(self.root_path + c3d_file_path, 'rb')
        except IOError as e:
            print("Couldn't open or write to file (%s)." % e)

        _columns = ["Marker_0:0:0 X", "Marker_0:0:0 Y", "Marker_0:0:0 Z", 
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
                    "Marker_3:3:4 X", "Marker_3:3:4 Y", "Marker_3:3:4 Z"]

        reader = c3d.Reader(file_c3d)
        c3d_df = pd.DataFrame(columns=_columns)

        for i, points, analog in tqdm(reader.read_frames()):
            _row_data = [points[0][0], points[0][1], points[0][2],
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
                        points[35][0], points[35][1], points[35][2]]

            zipped_data = dict(zip(_columns, _row_data))
            c3d_df = c3d_df.append(zipped_data, ignore_index=True)

        return c3d_df

    def add_timestamp(self, c3d_df, summary_filename:str, output_file:str, fixed_row=65):
        #df = pd.read_csv(c3d_filename)
        df_timestamp = pd.read_csv(self.root_path + summary_filename, skiprows=fixed_row)

        timestamp = df_timestamp["Time(sec)"]
        #df.insert(0, "timestamp", timestamp)
        #df.to_csv(self.output_dir+output_file)
        c3d_df.insert(0, "timestamp", timestamp)
        c3d_df.to_csv(self.save_path + output_file)

def main():
    root_path = ".\\sample\\"
    save_path = ".\\sample\\outputdir\\"
    c3d_file = "C3dExport.c3d"
    summary_file = "CsvExport_200514.csv"
    output_file = "jointinfo_timestamp2.csv"

    gears_post_processor = GearsPostProcess(root_path, save_path)
    c3d2csv_df = gears_post_processor.write_C3D2DF(c3d_file)
    gears_post_processor.add_timestamp(c3d2csv_df, summary_file, output_file)

    print("Process Done")

if __name__=="__main__":
    main()