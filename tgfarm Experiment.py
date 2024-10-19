import sys
from colorama import Fore, Style, init
from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError, ChatWriteForbiddenError, UserBannedInChannelError, FloodWaitError
import asyncio
import time
import os
import urllib.request
import json
import gzip
import inspect

version = "1.3"
os.system(f"title GSP {version}")

init()

# Переменные для сохранения данных аккаунта
api_id = None
api_hash = None
phone = None
client = None
message = None
delay = None
quantity = None

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
start_color2 = "#fa0000"
end_color2 = "#ffb8b8"
start_color3 = "#a89a00"
end_color3 = "#ede697"
start_color4 = "#01e952"
end_color4 = "#9ffec0"
start_color5 = "#ffffff"
end_color5 = "#878787"
start_color6 = "#1dacd6"
end_color6 = "#006d5b"
text_with_version = f"        Version: {version}"
clear_console()
# Лого
def display_logo():
    clear_console()
    text = f"""
		  ▄████   ██████  ██▓███  
		 ██▒ ▀█▒▒██    ▒ ▓██░  ██▒
		▒██░▄▄▄░░ ▓██▄   ▓██░ ██▓▒
		░▓█  ██▓  ▒   ██▒▒██▄█▓▒ ▒
		░▒▓███▀▒▒██████▒▒▒██▒ ░  ░
		 ░▒   ▒ ▒ ▒▓▒ ▒ ░▒ ▓▒░ ░  ░
		  ░   ░ ░ ░▒  ░ ░░▒ ░     
		  ░   ░ ░  ░  ░  ░           
           {text_with_version}
"""
    print(gradient_text(text, start_color, end_color))


#probiv

def provib_telefona():
    clear_console()
    display_logo()
    # Основной скрипт для получения информации о номере телефона
    print(gradient_text("   If it not sending info, you has no requests, wait 1 day", start_color5, end_color5))
    phone = input("     Enter phone: ")
    url = f"https://htmlweb.ru/geo/api.php?json&telcod={phone}"
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 OPR/114.0.0.0',
        'cookie': '_ym_uid=1729004468289199580; _ym_d=1729004468; _ym_isad=2; adtech_uid=%3Ahtmlweb.ru; top100_id=t1.1367185.817918808.1729004468282; t3_sid_1367185=s1.538624146.1729004468283.1729004472819.1.4'
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            if response.info().get('Content-Encoding') == 'gzip':
                with gzip.GzipFile(fileobj=response) as f:
                    data = f.read()
            else:
                data = response.read()

        infoPhone = json.loads(data.decode('utf-8'))

        # Проверка наличия ключей в ответе перед выводом данных
        print(gradient_text(f"Номер сотового ---> +{phone}", start_color5, end_color5))

        if "country" in infoPhone:
            country_info = infoPhone.get("country", {})
            print(gradient_text(f"Страна ---> {country_info.get('name', 'Неизвестно')}", start_color5, end_color5))
            print(gradient_text(f"Часть света ---> {country_info.get('location', 'Неизвестно')}", start_color5, end_color5))

        if "region" in infoPhone:
            region_info = infoPhone.get("region", {})
            print(gradient_text(f"Регион ---> {region_info.get('name', 'Неизвестно')}", start_color5, end_color5))
            print(gradient_text(f"Округ ---> {region_info.get('okrug', 'Неизвестно')}", start_color5, end_color5))
            input("Enter to back")

        if "0" in infoPhone:
            operator_info = infoPhone.get("0", {})
            print(gradient_text(f"Оператор ---> {operator_info.get('oper', 'Неизвестно')}", start_color5, end_color5))
            input("Enter to back")

    except Exception as e:
        print(f"[!] - Phonenot found - [!]: {e}")
        input("Enter to back")

        # Для отладки: выводим весь JSON-ответ, если он был успешно получен
        if 'infoPhone' in locals():
            print(gradient_text("JSON - ответ:", start_color5, end_color5) + json.dumps(infoPhone, ensure_ascii=False, indent=4))
            input("Enter to back")
        else:
            print(gradient_text("No valid JSON response received.", start_color5, end_color5))
            input("Enter to back")

def main_menu():
    clear_console()
    display_logo()
    print(gradient_text("		[S] Start", start_color4, end_color4))
    print(gradient_text("		[P] Check Number", start_color6, end_color6))
    print(gradient_text("		", start_color3, end_color3))
    print(gradient_text("		[C] Credits", start_color3, end_color3))
    print(gradient_text("		[E] Exit", start_color2, end_color2))
    print(" ")
    print(" ")

async def login_to_account(api_id, api_hash, phone):
    global client
    client = TelegramClient('anon', api_id, api_hash)
    await client.start(phone)
    me = await client.get_me()
    clear_console()
    display_logo()
    print(f"{Fore.GREEN}[+] Logged as {me.username}{Style.RESET_ALL}")



async def join_and_send_message():
    global client
    try:
        async for dialog in client.iter_dialogs():
            if dialog.is_group:
                try:
                    print(f"{Fore.GREEN}[+] Group parsed: @{dialog.entity.username}{Style.RESET_ALL}")
                    for _ in range(quantity):
                        await client.send_message(dialog.entity, message)
                        print(f"{Fore.GREEN}[+] {dialog.name} Sended message{Style.RESET_ALL}")
                        time.sleep(delay)  # Задержка между сообщениями
                except ChatWriteForbiddenError:
                    print(f"{Fore.RED}[-] {dialog.name} Closed{Style.RESET_ALL}")
                except UserBannedInChannelError:
                    print(f"{Fore.RED}[-] {dialog.name} Banned{Style.RESET_ALL}")
                except FloodWaitError as e:
                    print(f"{Fore.RED}[-] {dialog.name} Wait {e.seconds} {Style.RESET_ALL}")
                    continue  # Переход к следующей группе
    except Exception as e:
        print(f"{Fore.RED}[-] Can't logged: {str(e)}{Style.RESET_ALL}")
    finally:
        await client.disconnect()
        
        
        

async def send_messages_to_contacts():
    global client
    try:
        async for dialog in client.iter_dialogs():
            if dialog.is_user and not dialog.entity.bot:
                try:
                    print(f"{Fore.GREEN}[+] Contact parsed: {dialog.name}{Style.RESET_ALL}")
                    await client.send_message(dialog.entity, message)
                    print(f"{Fore.GREEN}[+] Message sent to {dialog.name}{Style.RESET_ALL}")
                    time.sleep(delay)  # Задержка между сообщениями
                except Exception as e:
                    print(f"{Fore.RED}[-] Failed to send message to {dialog.name}: {str(e)}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[-] Can't send messages to contacts: {str(e)}{Style.RESET_ALL}")
    finally:
        await client.disconnect()

def dev_mode():
    clear_console()
    display_logo()
    print(gradient_text("        DEV CHECK", start_color5, end_color5))
    print(gradient_text(text_with_version, start_color5, end_color5))
    print(gradient_text("        Color test:", start_color5, end_color5))
    print(gradient_text("████████████████████████ purple", start_color, end_color))
    print(gradient_text("████████████████████████ red", start_color2, end_color2))
    print(gradient_text("████████████████████████ yellow", start_color3, end_color3))
    print(gradient_text("████████████████████████ green", start_color4, end_color4))
    print(gradient_text("████████████████████████ white", start_color5, end_color5))
    print(gradient_text("████████████████████████ aqua", start_color6, end_color6))
    input(" ")

#devmde

def show_credits():
    clear_console()
    display_logo()
    print(" ")
    print(gradient_text("		GroupSpammer TG", start_color5, end_color5))
    print(gradient_text("		Send message to Groups/Contacts", start_color5, end_color5))
    print(gradient_text("		Created by @Ewinnery", start_color5, end_color5))
    input(" ")

if __name__ == '__main__':
    while True:
        display_logo()
        main_menu()
        option = input("			Select: ").strip().upper()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        if option == 'S':
            # Ввод данных для входа
            clear_console()
            display_logo()
            print(" ")
            print(gradient_text("		Enter Info", start_color5, end_color5))
            print(gradient_text("		Skip Api/Hash only when created session", start_color5, end_color5))
            print(gradient_text("		Enter 1 to skip Api/Hash", start_color5, end_color5))
            print(" ")
            api_id = input(gradient_text("Api Id:", start_color5, end_color5))
            api_hash = input(gradient_text("Api Hash:", start_color5, end_color5))
            phone = input(gradient_text("Number (+7):", start_color5, end_color5))
            loop.run_until_complete(login_to_account(api_id, api_hash, phone))
            clear_console()
            display_logo()

            # Ввод данных для сообщений
            message = input("		Message:  ")
            delay = float(input("		Send delay: "))
            quantity = int(input("		Message quanity: "))

            target_option = input("		[C/G] Contacts / Groups: ").strip().upper()
            if target_option == 'C':
                loop.run_until_complete(send_messages_to_contacts())
            elif target_option == 'G':
                loop.run_until_complete(join_and_send_message())
            else:
                print("		[?] Enter C/G to select")

        elif option == 'C':
            show_credits()
            clear_console()
            continue

        elif option == 'E':
            clear_console()
            display_logo()
            print(" ")
            print(gradient_text("Exited...", start_color2, end_color2))
            time.sleep(1)
            sys.exit()

        elif option == 'P':
            provib_telefona()

        elif option == 'DEV':
            dev_mode()

        else:
            print("		[!] Error, select in menu")
            clear_console()
            continue


           