import pyautogui
import time
import random

pyautogui.PAUSE = 1
pyautogui.FAILSAFE = True

filePos = open('C:\\Users\\arts\\Documents\\Web Scrapping\\position.txt', 'r')
coord = filePos.readlines()
filePos.close()
top = int(input('Number of hands:'))
number = 0  # start from 1
# add finding "START" element and then click relative position of hand.
while number < top: #

    el = number % 20 + 1
    if el == 1:
        pyautogui.screenshot()
        start = pyautogui.locateOnScreen('C:\\Users\\arts\\Documents\\Web Scrapping\\start.PNG',
                                confidence=0.8)
        x, y = pyautogui.center(start)
        
    xr = random.uniform(5, 15)
    yr = random.uniform(35.5, 36.1)
    time.sleep(0.2)
    print(yr, el*yr)
    
    pyautogui.moveTo(x+xr, y+el*yr, duration=random.uniform(0.0, 0.25))
    pyautogui.click()
    
    time.sleep(0.5)
    pyautogui.hotkey('ctrl','s')
    pyautogui.typewrite('hand' + str(number+1))
    pyautogui.press('enter')
    time.sleep(0.2)
    pyautogui.press('esc')

    if el == 20:
        next = pyautogui.locateOnScreen('C:\\Users\\arts\\Documents\\Web Scrapping\\next.png',
                                confidence = 0.8)
        pyautogui.click(pyautogui.center(next))
        
    number += 1
