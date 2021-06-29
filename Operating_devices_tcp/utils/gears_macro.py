# gears_macro.py

# This is the code for Gears Macro Program
# 20210629 Young-hoon Ji 

import os
import time
import pyautogui
import pygetwindow as gw

def gears_save(save_dir, file_counter):
    if(os.path.exists(save_dir)==False):
        os.mkdir(save_dir)
        
    csv_ext = ".csv"
    c3d_ext = ".c3d"

    win_gears = gw.getWindowsWithTitle("Gears - Sports")[0]
    win_gears.activate()

    pyautogui.moveTo(459, 22) # open data container
    pyautogui.click()
    pyautogui.moveTo(897, 1047, duration=1) # export button
    pyautogui.click()
    pyautogui.moveTo(853, 20, duration=0.2) # tap to change c3d and csv
    pyautogui.click()
    
    pyautogui.moveTo(821, 17, duration=0.2) # Point(x=821, y=17), file export option tab
    pyautogui.moveTo(833, 67, duration=0.2) # Point(x=833, y=67) csv file section
    pyautogui.click()

    # use  for loop to export csv
    for i in range(file_counter):
        base_x = 882
        base_y = 110
        delta_y = 25

        #win_gears.activate()
        pyautogui.moveTo(base_x, base_y, duration=0.2) # Point(x=897, y=173) change save dir
        pyautogui.click()
        time.sleep(1)
        
        #pyautogui.moveTo(base_x, base_y+delta_y*(i+1), duration=0.2) # Point(x=897, y=173) change save dir
        pyautogui.moveTo(base_x, base_y+delta_y*(i+1)) # Point(x=897, y=173) change save dir
        pyautogui.click()

        pyautogui.moveTo(897, 173, duration=0.2) # Point(x=897, y=173) change save dir
        pyautogui.click()
        pyautogui.typewrite(save_dir+"CsvExport_"+str(i)+csv_ext)
        time.sleep(1)
        pyautogui.moveTo(1181, 230, duration=0.2) # Point(x=1181, y=230) export button
        pyautogui.click()

    pyautogui.moveTo(821, 17, duration=0.2) # Point(x=821, y=17), file export option tab
    pyautogui.click()
    pyautogui.moveTo(833, 90, duration=0.2) # Point(x=833, y=67) c3d file section
    pyautogui.click()

    for i in range(file_counter):
        base_x = 882
        base_y = 110
        delta_y = 25

        pyautogui.moveTo(base_x, base_y, duration=0.2) # Point(x=897, y=173) tab number of capture
        pyautogui.click()
        time.sleep(1)

        #pyautogui.moveTo(base_x, base_y+delta_y*(i+1), duration=0.2) # Point(x=897, y=173) change save dir
        pyautogui.moveTo(base_x, base_y+delta_y*(i+1)) # Point(x=897, y=173) change save dir
        pyautogui.click()

        pyautogui.moveTo(897, 173, duration=0.2) # Point(x=897, y=173) change save dir
        pyautogui.click()
        pyautogui.typewrite(save_dir+"C3DExport_"+str(i)+c3d_ext)
        time.sleep(1)
        pyautogui.moveTo(1181, 230, duration=0.2) # Point(x=1181, y=230) export button
        pyautogui.click()

    pyautogui.moveTo(1047, 230, duration=0.2) # Point(x=1047, y=230), close saving tab
    pyautogui.click()
    pyautogui.moveTo(1895, 17, duration=0.2) # Point(x=1895, y=17), close saving tab
    pyautogui.click()    

if __name__=="__main__":
    save_dir = "C:\\Users\\GEARS\\Desktop\\GEARS_Data_PostProcess\\okay2del\\210629\\test3\\"
    counter = 2

    gears_save(save_dir, counter)

