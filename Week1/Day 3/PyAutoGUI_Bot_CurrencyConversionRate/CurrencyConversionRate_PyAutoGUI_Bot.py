#---------------------------------------------
# This BOT automates the process of caputuring the EUR to INR conversion rate from Google search, 
# saving it in a Notepad file, and taking a screenshot of the Notepad file.
#---------------------------------------------

import pyautogui
import time
from datetime import datetime

#---------------------------------------------
# Path configuration
#---------------------------------------------
#file_name = "DailyCurrencyConversionReport"
folder_path = r"C:\Users\vigne\Downloads\DailyCurrencyConversionReport"

today_date = datetime.now().strftime("%Y-%m-%d")

file_path = folder_path + "_" + today_date + ".txt"
screenshot_save_path = folder_path + "_" + today_date + ".png"
#---------------------------------------------
# Step 1: Open Chrome browser
#---------------------------------------------

pyautogui.hotkey('win', 'r')  # Open the Run dialog
time.sleep(1)
pyautogui.typewrite("chrome", interval=0.1)
pyautogui.press('enter')

#---------------------------------------------
#Step 2: Search for EUR to INR conversion rate
#---------------------------------------------
time.sleep(2)
pyautogui.typewrite("EUR to INR", interval=0.1)
pyautogui.press('enter')

#---------------------------------------------
#Step 3: Copy the conversion rate
#---------------------------------------------
time.sleep(3)  
pyautogui.moveTo(400, 820)  # Move to the location of the conversion rate (adjust coordinates as needed)
pyautogui.doubleClick()  
pyautogui.hotkey('ctrl', 'c')  
time.sleep(3)

#---------------------------------------------
#Step 4: Open Excel and paste the conversion rate
#---------------------------------------------

pyautogui.hotkey('win', 'r')  # Open the Run dialog
time.sleep(1)
pyautogui.typewrite("notepad", interval=0.1)
pyautogui.press('enter')
time.sleep(5)

#pyautogui.hotkey('ctrl', 'n')  
#time.sleep(2)
pyautogui.typewrite(datetime.now().strftime("%Y-%m-%d %H-%M-%S"), interval=0.1)  
pyautogui.press('tab')  
pyautogui.hotkey('ctrl', 'v')  
pyautogui.press('tab')  
pyautogui.press('tab')  
pyautogui.typewrite("Conversion rate captured Successfully", interval=0.1)  

pyautogui.hotkey('ctrl', 's')  
time.sleep(2)
pyautogui.typewrite(file_path, interval=0.1)  
pyautogui.press('enter')

#---------------------------------------------
#Step 5: Save a screenshot of the Notepad file
#---------------------------------------------
time.sleep(2)
pyautogui.screenshot(screenshot_save_path)  # Save a screenshot of the Notepad file
time.sleep(2)

print("Daily currency conversion report generated and saved successfully.")