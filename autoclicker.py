import sys
import tkinter as tk
from tkinter import messagebox as mb
from tkinter import OptionMenu
from tkinter import StringVar
import time
import threading
from pynput.mouse import Button, Controller
from pynput.keyboard import Key, Listener, KeyCode
from pynput.keyboard import Controller as KeyCont

mouse = Controller()
keyboard = KeyCont()

class ClickMouse(threading.Thread):
    def __init__(self, delay, button):
        super(ClickMouse, self).__init__()
        self.delay = delay
        self.button = button
        self.running = False
        self.program_running = True

    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self.running = False

    def exit(self):
        self.stop_clicking()
        self.program_running = False
        self.join()

    def run(self):
        while self.program_running:
            while self.running:
                mouse.click(self.button)
                time.sleep(self.delay)
            time.sleep(0.1)


class KeybaordListen(threading.Thread):
    def __init__(self, click_thread, start_stop_key):
        super(KeybaordListen, self).__init__()
        self.click_thread = click_thread
        self.start_stop_key = start_stop_key
        self.running = False
        self.program_running = True


    def on_press(self,key):
        if key == self.start_stop_key:
            if self.click_thread.running:
                self.click_thread.stop_clicking()
            else:
                self.click_thread.start_clicking()
        if key == Key.f10:
            return False

        

    def exit(self):
        self.program_running = False
        self.running = False
        keyboard.press(Key.f10)
        self.join()
        sys.exit()

    def run(self):
        while self.program_running:
            with Listener(on_press=self.on_press) as listener:
                listener.join()
                

def invalid():
    mb.showerror("Error", f"Start and Click delay can only be an float!")


def checkKey(key):
    if(len(key) > 1):
        mb.showerror("Error", f"Enter a valid key!")
        return False
    else:
        return True

def checkNum(cd):
    try:
        float(cd)
        return True
    except ValueError:
        invalid()
        return False





def start_clicking(cd, btn, key):
    button = Button.left
    if btn == 'right':
        button = Button.right
    if btn == 'middle':
        button = Button.middle
    if btn == 'left':
        button = Button.left
    start_stop_key = KeyCode(char=key)
    click_thread = ClickMouse(cd, button)
    click_thread.start()
    keyboard_thread = KeybaordListen(click_thread,start_stop_key)
    keyboard_thread.start()
    mb.showinfo("Info",f"Task started, Click {key} to start autoclicker")




def check_start():
    cd = str(e2.get())
    btn = str(button_variable.get())
    key = str(e3.get())
    if (checkNum(cd) and checkKey(key)):
        cd = float(cd)
        start_clicking(cd, btn, key)
        return True
    else:
        return False

def quitAll():
    for thread in threading.enumerate():
        if not(thread.getName()=='MainThread'):
            thread.exit()
    sys.exit()

master = tk.Tk()
master.title('Autoclicker')

button_choices = ['middle', 'left', 'right']
button_variable = StringVar(master)
button_variable.set('left')

tk.Label(master,
         text="Click Delay (sec)").grid(row=0)
tk.Label(master,
         text="Start/Stop Button").grid(row=1)

op = OptionMenu(master, button_variable, *button_choices)
e2 = tk.Entry(master)
e3 = tk.Entry(master)
e2.grid(row=0, column=1)
e3.grid(row=1, column=1)
op.grid(row=0, column=2)

tk.Button(master,
          text='Quit',
          command=quitAll).grid(row=3,
                                    column=0,
                                    sticky=tk.W,
                                    pady=4)
tk.Button(master,
          text='Start', command=check_start).grid(row=3,
                                                  column=1,
                                                  sticky=tk.W,
                                                  pady=4)

tk.mainloop()