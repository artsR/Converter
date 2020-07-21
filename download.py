import pyautogui
import time
import random

pyautogui.PAUSE = 1
pyautogui.FAILSAFE = True

basedir = os.path.abspath(os.path.dirname(__file__))


filePos = open(os.path.join(basedir, 'position.txt'), 'r')
coord = filePos.readlines()
filePos.close()
top = int(input())
number = 1  # start from 1

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
    next = pyautogui.locateOnScreen(os.path.join(basedir, 'next.png'), confidence = 0.8)
    pyautogui.click(pyautogui.center(next))
