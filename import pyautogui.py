import pyautogui
import time
pyautogui.FAILSAFE = False

#print(pyautogui.size())
print(pyautogui.position())
#pyautogui.moveTo(396,294)
#pyautogui.moveTo(398,320)
#difference between the two cells is approximately 26(vertical direction going downward)
#pyautogui.moveTo(398,346)

""""
pyautogui.moveTo(0, 1079)
pyautogui.moveTo(1231, 394)
pyautogui.click(x=0, y=1079, clicks=1, button='left')
pyautogui.typewrite('Telegram', interval=0)
pyautogui.typewrite(['enter'], interval=0)
pyautogui.click(x=51, y=59, clicks=1, button='left')
time.sleep(1)
pyautogui.click(x=51, y=59, clicks=1, button='left')
time.sleep(1)
pyautogui.click(x=116, y=330, clicks=1, button='left')
time.sleep(1)
#check here it is missing the spot
pyautogui.click(x=809, y=861, clicks=1, button='left')
time.sleep(1)
pyautogui.typewrite('Eyoel', interval=0)
pyautogui.click(x=844, y=520, clicks=1, button='left')
pyautogui.typewrite('Mekonnen', interval=0)
pyautogui.click(x=874, y=623, clicks=1, button='left')
pyautogui.typewrite('944067638', interval = 0)

"""