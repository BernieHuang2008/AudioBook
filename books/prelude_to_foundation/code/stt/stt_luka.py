# https://www.reccloud.cn/ai-subtitle

import pyautogui
import time


def stt(day):
    # nav to the audioTransfer page
    pyautogui.moveTo(658, 579)
    pyautogui.click()
    pyautogui.moveTo(883, 797)
    pyautogui.click()

    # wait and upload
    time.sleep(0.7)
    pyautogui.moveTo(609, 234)
    pyautogui.click()
    for _ in range(day - 1):
        pyautogui.press("down")
    pyautogui.press("enter")

    # wait for opening
    time.sleep(4)
    pyautogui.moveTo(2064, 696)
    pyautogui.click()

    # run js code
    pyautogui.press("f12")
    time.sleep(0.5)
    pyautogui.moveTo(2126, 130)
    pyautogui.click()
    pyautogui.moveTo(2133, 905)
    pyautogui.click()
    code = (
        f"const day={day};"
        + """
    function getsrt() {
        srt='';
        document.querySelectorAll('#text-area-id > ul > li').forEach(e=>{e=e.children[0];srt+=`0\\n${e.children[0].innerText.replace('-', '--->')}\\n${e.children[1].innerText}\\n\\n`});
        return srt;
    }
    function download(filename, text) {
        var element = document.createElement('a');
        element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
        element.setAttribute('download', filename);
        element.style.display = 'none';
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
    }
    function trydl() {
        if (document.querySelector('#text-area-id > ul > li'))
            download(`prelude_to_foundation-${day}.srt`, getsrt());
        else
            setTimeout(trydl, 1000);
    }
    trydl();
    """
    )
    pyautogui.typewrite(code)
    pyautogui.press("enter")
    time.sleep(10)
    pyautogui.press("f12")


# time.sleep(3), stt(5)
# time.sleep(3), print(f"pyautogui.moveTo({pyautogui.position().x}, {pyautogui.position().y})")
time.sleep(5)
for i in range(19, 63+1, 3):  # 63+1
    # change new inprivate window
    pyautogui.moveTo(2520, 7)
    pyautogui.click()
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'shift', 'n')
    time.sleep(1)
    pyautogui.typewrite("https://www.reccloud.cn/ai-subtitle")
    pyautogui.press("enter")
    time.sleep(2)
    for j in range(i, i+3):
        time.sleep(1)
        stt(j)
        time.sleep(12)
        pyautogui.moveTo(173, 68)
        pyautogui.click()
