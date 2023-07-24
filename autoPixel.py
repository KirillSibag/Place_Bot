import pyautogui, random
from time import sleep

f = open("result.txt")

data = f.readlines()

diction = []
for i in data:
    a = str(i)
    diction.append(a[0:len(i)-1])

for i in diction:
    sleep(22)
    pyautogui.typewrite(i, interval=0.0)
    pyautogui.press('enter')
