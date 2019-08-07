import pyautogui
import time
import random

pyautogui.PAUSE = 1
pyautogui.FAILSAFE = True

filePos = open('C:\\Users\\arts\\Documents\\Web Scrapping\\position.txt', 'r')
coord = filePos.readlines()
filePos.close()
top = int(input())
number = 1  # start from 1
# add finding "START" element and then click relative position of hand.
while number < top: #

    for coo in coord:
        x,y = coo.split(',')
        pyautogui.moveTo(int(x), int(y), duration=random.uniform(0.0, 0.25))
        pyautogui.click()
        time.sleep(0.5)
        pyautogui.hotkey('ctrl','s')
        pyautogui.typewrite('hand' + str(number))
        pyautogui.press('enter')
        time.sleep(0.2)
        pyautogui.press('esc')
        number += 1
    pyautogui.screenshot()
    next = pyautogui.locateOnScreen('C:\\Users\\arts\\Documents\\Web Scrapping\\next.png',
                                confidence = 0.8)
    pyautogui.click(pyautogui.center(next))
