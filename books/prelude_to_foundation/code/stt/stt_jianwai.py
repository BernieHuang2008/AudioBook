import pyautogui
import time

def stt(day):
    # nav to the audioTransfer page
    pyautogui.moveTo(2155, 348)
    pyautogui.click()
    pyautogui.moveTo(1080, 975)
    pyautogui.click()

    # fill in the title
    pyautogui.moveTo(904, 559)
    pyautogui.click()
    pyautogui.typewrite(f"prelude_to_foundation-{day}")

    # fill in the output type
    pyautogui.moveTo(841, 963)
    pyautogui.click()
    pyautogui.moveTo(784, 1065)
    pyautogui.click()

    # load audio file
    pyautogui.moveTo(841, 688)
    pyautogui.click()
    time.sleep(0.3)
    pyautogui.moveTo(609, 234)
    pyautogui.click()
    for _ in range(day-1):
        pyautogui.press("down")
    pyautogui.press("enter")

    # submit
    time.sleep(7)
    pyautogui.moveTo(841, 1086)
    pyautogui.click()

time.sleep(3)
# print(pyautogui.position())
for i in range(5, 8+1):  # 63+1
    stt(i)
    time.sleep(10)

