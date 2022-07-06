# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import win32api, win32con
import pymem
from pymem.process import module_from_name
from pymem.ptypes import RemotePointer
import pydirectinput
from PIL import ImageGrab
import keyboard
from win32gui import GetWindowText, GetForegroundWindow
import time
def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

def shiftClick(x,y):


    pydirectinput.keyDown('shift')
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
    pydirectinput.keyUp('shift')


def rightClick(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y,0,0)


def move(dir): # 0 gora, 1 dol, 2 prawo, 3 lewo
    if (dir == 0):
        pydirectinput.keyDown('w')
        pydirectinput.keyDown('a')
        pydirectinput.keyUp('w')
        pydirectinput.keyUp('a')
    elif (dir == 1):
        pydirectinput.keyDown('s')
        pydirectinput.keyDown('d')
        pydirectinput.keyUp('s')
        pydirectinput.keyUp('d')
    elif (dir == 2):
        pydirectinput.keyDown('w')
        pydirectinput.keyDown('d')
        pydirectinput.keyUp('w')
        pydirectinput.keyUp('d')
    elif (dir == 3):
        pydirectinput.keyDown('s')
        pydirectinput.keyDown('a')
        pydirectinput.keyUp('s')
        pydirectinput.keyUp('a')

def gotoSafeArea():
    if GetWindowText(GetForegroundWindow()) == 'Diablo Immortal':
        #print(GetWindowText(GetForegroundWindow()))
        pydirectinput.keyDown('b')
        pydirectinput.keyUp('b')
        time.sleep(0.5)
        click(1325, 992)
        time.sleep(0.5)
        click(1307, 896)

def sellEq(): # morze sasarskie
    if GetWindowText(GetForegroundWindow()) == 'Diablo Immortal':
        gotoSafeArea()
        time.sleep(20)
        click(1096, 658)
        time.sleep(30)
        click(1851, 74)
        time.sleep(3)

        click(183,260)
        time.sleep(6)
        click(1497, 669)
        time.sleep(1)
        click(784, 974)
        time.sleep(0.2)
        click(876, 974)
        time.sleep(0.2)
        click(960, 974)
        time.sleep(1)
        click(1472, 945)
        time.sleep(1)
        click(1851, 74)
        time.sleep(1)
        rightClick(1438, 702)
        time.sleep(0.01)
        rightClick(1438, 702)
        time.sleep(5)
        click(1576, 528)
        time.sleep(10)



def checkHealth():
    if GetWindowText(GetForegroundWindow()) == 'Diablo Immortal':
        im = ImageGrab.grab(bbox=(123, 134, 124, 135))
        #im.show()
        pix = im.load()
        #print(im.size)
        if pix[0, 0] == (0, 0, 0):
            pydirectinput.keyDown('q')
            pydirectinput.keyUp('q')

def isFulleq():
    if GetWindowText(GetForegroundWindow()) == 'Diablo Immortal':
        pydirectinput.keyDown('b')
        pydirectinput.keyUp('b')
        time.sleep(1)
        im = ImageGrab.grab(bbox=(1485, 950, 1486, 951))
        #im.show()
        pix = im.load()
        print(pix[0, 0])
        if pix[0, 0] == (130, 27, 23) or pix[0, 0] == (151, 111, 38):
            time.sleep(1)
            click(1850, 50)
            return True
        time.sleep(1)
        click(1850, 50)
        return False

if __name__ == '__main__':
    isStarted = False
    while isStarted:
        if keyboard.is_pressed('l'):  # if key 'q' is pressed
            print('You Pressed A Key!')
            #break
            #checkHealth()
            sellEq()


def resolvePointer(handler, base, offsets):
    last = base
    for offset in offsets:
        last = RemotePointer(handler, last.value + offset)
    return last.v.value


pm = pymem.Pymem("DiabloImmortal.exe")
gameModule = module_from_name(pm.process_handle, "DiabloImmortal.exe").lpBaseOfDll

initialPointer = gameModule + 0x0351EB98
offsets = {
    "xPos": [0x118, 0xA00, 0x28, 0x1F0, 0x28, 0x28, 0xC8],
    "yPos": [0x118, 0xA00, 0x28, 0x1F0, 0x28, 0x28, 0xD0],
}

values = {}
startB = True
waypoints = {
    "exp": [(-17, 0), (1, -3), (15, -4), (15, -24), (13, -35), (-15, -35), (-16, -19)],
    "morze": [
        (110, -78), (132, -78), (132, -65), (119, -64), (119, -53), (130, -52), (129, -34), (110, -34),
        (113, -52), (119, -52), (119, -64),  (110, -64), (110, -68), (75, -68), (110, -68)
              ]
}
chosenWaypoints = "morze"
state = 0
up = False
down = False
left = False
right = False
fightArea = False
checkEQ = False
start = time.time()
while startB:
    pause = False
    try:  # used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('l'):  # if key 'q' is pressed
            print('You Pressed A Key!')
            break  # finishing the loop
    except:
        break  # if user pressed a key other than the given key the loop will break
    for offset in offsets:
        offsetList = offsets.get(offset)
        pointer = RemotePointer(pm.process_handle, initialPointer)

        val = 0
        try:
            address = resolvePointer(pm.process_handle, pointer, offsetList)
            val = pm.read_float(address)
        except Exception:
            pass
        values[offset] = val
    #print(values)
    if GetWindowText(GetForegroundWindow()) != 'Diablo Immortal':
        continue
    checkHealth()
    if state == 14:
        time.sleep(3)
        pydirectinput.keyDown('4')
        pydirectinput.keyUp('4')
        time.sleep(3)
        shiftClick(1334, 750)
        pydirectinput.keyDown('3')
        pydirectinput.keyUp('3')
        state = 0
        checkHealth()
        time.sleep(3)
    im = ImageGrab.grab(bbox=(300, 0, 1550, 900))
    # im.show()
    pix = im.load()
    pydirectinput.keyDown('3')
    pydirectinput.keyUp('3')

    for y in range(0, im.size[1], 5):
        isBreak = False
        for x in range(0, im.size[0], 5):
            color = pix[x, y]
            if color == (149, 20, 20):
                shiftClick(300 + x + 20, y + 120)
                pydirectinput.keyDown('1')
                pydirectinput.keyUp('1')
                pydirectinput.keyDown('2')
                pydirectinput.keyUp('2')
                pydirectinput.keyDown('4')
                pydirectinput.keyUp('4')
                pause = True
                isBreak = True
                break
        if isBreak:
            break
    if pause == False and checkEQ:
        time.sleep(2.5)
        sellEq()
        checkEQ = False
    if checkEQ:
        state = 13
    if pause or checkEQ:
        continue
    r = 3
    gitX = False
    gitY = False
    if values['xPos'] > (waypoints[chosenWaypoints][state][0]-r) and values['xPos'] < (waypoints[chosenWaypoints][state][0]+r):
        gitX = True
        #print('helloxDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD')
    elif values['xPos'] > (waypoints[chosenWaypoints][state][0]-r):
        # 180 + 45 stopni
        click(960 - 170, 540 + 190)
        rightClick(960 - 170, 540 + 190)
        #move(3)


    else:
        #click 45 stopni
        click(960 + 200, 540 - 120)
        rightClick(960 + 200, 540 - 120)
        #move(2)


    if values['yPos'] > (waypoints[chosenWaypoints][state][1]-r) and values['yPos'] < (waypoints[chosenWaypoints][state][1]+r) and gitX:
        #print('git Y')
        gitY = True
    elif values['yPos'] > (waypoints[chosenWaypoints][state][1]-r) and gitX:
        click(960 - 150, 540 - 180)
        rightClick(960 - 150, 540 - 180)
        #move(0)
        #print('gora')
    elif gitX:
        click(960 + 190, 540 + 220)#3
        rightClick(960 + 190, 540 + 220)#3
        #move(1)
        #1print('down')
    if gitY and gitX:
        state += 1
        start = time.time()
        end = time.time()
    if state == 14:
        print('stop tutaj check eq')
        checkEQ = isFulleq()
        print(checkEQ)

    #print(state)
    end = time.time()
    checkTime = end-start
    print(end - start)
    if checkTime > 120:
        state += 1
        start = time.time()
        end = time.time()
        click(1386, 791)
    if state == 15:
        state = 0
    #time.sleep(0.1)