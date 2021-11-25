import os
import urllib.request as API
import zipfile
import re
import socket
import shutil
os.system('title SurfShark OVPN Merger By Incognito Coder')
os.system('cls' if os.name == 'nt' else 'clear')


class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


print(f'{colors.OKCYAN}\n'
      ' o-o  o   o o--o  o--o  o-o  o  o   O  o--o  o  o      o-o  o--o  o--o o   o o   o o--o  o   o \n'
      '|     |   | |   | |    |     |  |  / \ |   | | /      o   o |   | |    |\  | |   | |   | |\  | \n'
      ' o-o  |   | O-Oo  O-o   o-o  O--O o---oO-Oo  OO       |   | O--o  O-o  | \ | o   o O--o  | \ | \n'
      '    | |   | |  \  |        | |  | |   ||  \  | \      o   o |     |    |  \|  \ /  |     |  \| \n'
      'o--o   o-o  o   o o    o--o  o  o o   oo   o o  o      o-o  o     o--o o   o   o   o     o   o \n'
      f'{colors.ENDC}\n'
      f'{colors.HEADER}[+] This is a fork from SurfSocks project by Incognito Coder.{colors.ENDC}')
print("[+] ABOUT SCRIPT:")
print("[-] With this script, you can save U/P to openvpn configs and convert hostname to ip.")
print("[-] Version: 1.1")
print("--------")
print("[-] SITE: mr-incognito.ir")
print("[-] TELEGRAM: @ic_mods")
print("--------")


def assets():
    if os.path.isfile('Surfshark_Config.zip'):
        with zipfile.ZipFile("Surfshark_Config.zip", "r") as ziped:
            ziped.extractall(os.getcwd()+'/configs/')
    else:
        print('[!] Downloading resources from surfshark.')
        API.urlretrieve(
            'https://my.surfshark.com/vpn/api/v1/server/configurations', 'Surfshark_Config.zip')
        assets()


def runner():
    assets()
    username = input(f"{colors.BOLD}-> Enter Username : {colors.ENDC}")
    password = input(f"{colors.BOLD}-> Enter Password : {colors.ENDC}")
    if username == '' or password == '':
        print('Enter All Requirements.')
        exit
    else:
        print(f'{colors.WARNING}Starting ...{colors.ENDC}')
        files = os.listdir(os.getcwd()+'/configs/')
        compress = zipfile.ZipFile(
            'Merged-Configs.zip', 'w', zipfile.ZIP_DEFLATED)
        for file in files:
            with open(os.getcwd()+'/configs/'+file, 'r') as f:
                data = f.read()
                regex = re.compile("remote (.*?) ").search(data)
                data = data.replace(regex.group(
                    1), socket.gethostbyname(regex.group(1)))
                merged = data + \
                    f"<auth-user-pass>\n{username}\n{password}\n</auth-user-pass>"
                f.close()
            with open(os.getcwd()+'/configs/'+file, 'w') as f:
                f.write(merged)
                f.close()
                print(
                    f'{colors.OKGREEN}[?]{colors.ENDC} {file} {colors.OKGREEN}Merged Successfully.{colors.ENDC}')
            compress.write('configs/'+file)
        print(f'{colors.BOLD}[!] Cleaning workspace.{colors.ENDC}')
        shutil.rmtree(os.getcwd() + '/configs/')
        print(
            f'{colors.OKBLUE}[$] Files Saved as {colors.ENDC}Merged-Configs.zip')


runner()
