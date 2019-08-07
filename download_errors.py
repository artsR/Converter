import pyautogui
import time
import random
import re
import os

pyautogui.PAUSE = 1
pyautogui.FAILSAFE = True

filePos = open('C:\\Users\\arts\\Documents\\Web Scrapping\\position.txt', 'r')
coord = filePos.readlines()
filePos.close()
fileErr = open('C:\\Users\\arts\\Documents\\Web Scrapping\\errors.txt', 'r')
errors = fileErr.readlines()
fileErr.close()
hands_no = re.findall(r'\d+', ''.join(errors))
hands_no = list(map(int, hands_no))

# Add missed numbers:
# ...hand200, hand202, .. - add hand201 to errors' list.
number_all = []
for file_hand in os.listdir():
    if file_hand.startswith('hand') and file_hand.endswith('.htm'):
        number_all.append(int(re.findall(r'\d+', file_hand)[0]))
last_hand = max(number_all)
for i in range(1, last_hand+1):
    if i not in number_all:
        hands_no.append(i)

hands_no.sort()
print(hands_no)

p = 0
for hand_no in hands_no:
    #-------------------------------------

    #-------------------------------------
    page_no = hand_no // 20
    item_no = hand_no % 20
    while True:
        if p == page_no:
            i = 1
            for coo in coord:
                x,y = coo.split(',')
                if i == item_no:
                    print(hand_no, page_no, p, item_no, i)
                    pyautogui.moveTo(int(x),int(y), duration=random.uniform(0.0, 0.25))
                    pyautogui.click()
                    time.sleep(1.5)
                    pyautogui.hotkey('ctrl','s')
                    pyautogui.typewrite('err_hand' + str(hand_no))
                    pyautogui.press('enter')
                    time.sleep(0.2)
                    pyautogui.press('esc')
                    break
                else:
                    i = i + 1
                    continue
            #if item_no == 0: # save 20th item of the page:
            #    print(hand_no, page_no, p, item_no, i)
            #    pyautogui.moveTo(int(x),int(y), duration=random.uniform(0.0, 0.25))
            #    pyautogui.click()
            #    time.sleep(1.5)
            #    pyautogui.hotkey('ctrl','s')
            #    pyautogui.typewrite('err_hand' + str(hand_no))
            #    pyautogui.press('enter')
            #    time.sleep(0.2)
            #    pyautogui.press('esc')

            break
        elif p > page_no:
            break
        else:
            pyautogui.screenshot()
            next = pyautogui.locateOnScreen('C:\\Users\\arts\\Documents\\Web Scrapping\\next.png',
                                    confidence = 0.8)
            pyautogui.click(pyautogui.center(next))
            p = p + 1
