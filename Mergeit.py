import os
import urllib.request as API
import zipfile
import re
import socket
import shutil
import time
import json
import subprocess
from configparser import ConfigParser
import webbrowser
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


config = ConfigParser()
config.read('config.ini')


def Main():
    print(f'{colors.OKCYAN}\n'
          ' o-o  o   o o--o  o--o  o-o  o  o   O  o--o  o  o      o-o  o--o  o--o o   o o   o o--o  o   o \n'
          '|     |   | |   | |    |     |  |  / \ |   | | /      o   o |   | |    |\  | |   | |   | |\  | \n'
          ' o-o  |   | O-Oo  O-o   o-o  O--O o---oO-Oo  OO       |   | O--o  O-o  | \ | o   o O--o  | \ | \n'
          '    | |   | |  \  |        | |  | |   ||  \  | \      o   o |     |    |  \|  \ /  |     |  \| \n'
          'o--o   o-o  o   o o    o--o  o  o o   oo   o o  o      o-o  o     o--o o   o   o   o     o   o \n'
          f'{colors.ENDC}\n'
          f'{colors.HEADER}[+] This is a fork from SurfSocks project by Incognito Coder.{colors.ENDC}\n'
          '[+] ABOUT SCRIPT:\n'
          '[-] With this script, you can save U/P to openvpn configs and convert hostname to ip\n'
          '[-] Version: 2.3\n'
          '--------\n'
          '[-] SITE: mr-incognito.ir\n'
          '[-] TELEGRAM: @ic_mods\n'
          '--------')
    print(f'{colors.HEADER}'
          '[1] Create/Update Configs\n'
          '[2] Save Default Username / Password\n'
          '[3] Clear Saved Username / Password\n'
          '[4] Delete Downloaded zip\n'
          '[5] Open Project Page'
          f'{colors.ENDC}\n')
    opt = input('Select an option: ')
    if opt == '1':
        runner()
    elif opt == '2':
        SaveUP()
    elif opt == '3':
        ClearUP()
    elif opt == '4':
        os.system('cls' if os.name == 'nt' else 'clear')
        try:
            os.remove(os.getcwd() + '/Surfshark_Config.zip')
            print('Removed Successfully.')
            time.sleep(1)

        except:
            print('Not Found.')
            time.sleep(1)
        Main()
    elif opt == '5':
        webbrowser.open('https://github.com/Incognito-Coder/SurfShark-OpenVPN')
        Main()
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Undefined option.Exiting ...')
        time.sleep(2)


def assets():
    if os.path.isfile('Surfshark_Config.zip'):
        with zipfile.ZipFile("Surfshark_Config.zip", "r") as ziped:
            ziped.extractall(os.getcwd()+'/configs/')
    else:
        try:
            print('[!] Downloading resources from surfshark.')
            API.urlretrieve(
                'https://my.surfshark.com/vpn/api/v1/server/configurations', 'Surfshark_Config.zip')
            assets()
        except:
            print('[!] Download error.')


def runner():
    os.system('cls' if os.name == 'nt' else 'clear')
    assets()
    username = None
    password = None
    try:
        username = config.get('default', 'user')
        password = config.get('default', 'pass')
    except:
        username = input(f"{colors.BOLD}-> Enter Username : {colors.ENDC}")
        password = input(f"{colors.BOLD}-> Enter Password : {colors.ENDC}")
        if username == '' or password == '':
            print('Enter All Requirements.')
            exit()
    print(f'{colors.WARNING}Starting ...{colors.ENDC}')
    files = os.listdir(os.getcwd()+'/configs/')
    compress = zipfile.ZipFile(
        'Merged-Configs.zip', 'w', zipfile.ZIP_DEFLATED)
    for file in files:
        with open(os.getcwd()+'/configs/'+file, 'r') as f:
            data = f.read()
            regex = re.compile("remote (.*?) ").search(data)
            ip = socket.gethostbyname(regex.group(1))
            data = data.replace(regex.group(
                1), ip)
            merged = data + \
                f"<auth-user-pass>\n{username}\n{password}\n</auth-user-pass>"
            f.close()
        try:
            ping = PingDelay(ip)
            with open(os.getcwd() + '/configs/' + file, 'w') as f:
                f.write(merged)
                f.close()
                print(
                    f'{colors.OKGREEN}[?]{colors.ENDC} {file} {colors.OKGREEN}Merged Successfully.{colors.ENDC} | Response : {colors.OKBLUE}{ping}{colors.ENDC}')
            time.sleep(2)
            JData = json.loads(API.urlopen(
                f'http://ip-api.com/json/{ip}').read())
            new_name = f"{JData['country']} - {JData['city']} ({ip}).ovpn"
            proto = re.compile(r"proto (.*)").search(merged)
            if proto.group(1) == 'udp':
                compress.write('configs/'+file, 'UDP/'+new_name)
            else:
                compress.write('configs/'+file, 'TCP/'+new_name)

        except:
            print(
                f'{colors.FAIL}[?] {file} Invalid Hostname or Server is Down.{colors.ENDC}')
            os.remove(os.getcwd() + '/configs/' + file)

    print(f'{colors.BOLD}[!] Cleaning workspace.{colors.ENDC}')
    shutil.rmtree(os.getcwd() + '/configs/')
    print(
        f'{colors.OKBLUE}[$] Files Saved as {colors.ENDC}Merged-Configs.zip')
    os.system("pause" if os.name ==
              'nt' else "read -rsp $'Press enter to exit...\n'")


def SaveUP():
    os.system('cls' if os.name == 'nt' else 'clear')
    username = input(f"{colors.BOLD}-> Enter Username : {colors.ENDC}")
    password = input(f"{colors.BOLD}-> Enter Password : {colors.ENDC}")
    try:
        config.add_section('default')
        config.set('default', 'user', username)
        config.set('default', 'pass', password)
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    except:
        config.set('default', 'user', username)
        config.set('default', 'pass', password)
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    print(f'{colors.OKBLUE}[$] Credentials Saved.{colors.ENDC}')
    time.sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear')
    Main()


def ClearUP():
    config.remove_section('default')
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    time.sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear')
    Main()


def PingDelay(host):
    if os.name == 'nt':
        time = subprocess.Popen(
            ['ping', host, '-n', '1'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output = time.communicate()
        pattern = re.findall(r"Average = (\d+\S+)", output[0].decode())[0]
    else:
        ping_response = subprocess.Popen(
            ["ping", "-c1", host], stdout=subprocess.PIPE).stdout.read()
        rexex = re.compile('time=(.*?) ms').search(str(ping_response)).group(1)
        pattern = rexex+'ms'
    return pattern


Main()
