import socket
import netifaces
from scapy.all import ARP, Ether, srp
import requests
import os

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# функция для градиентного текста
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

# цвета
start_color = "#ff7e93"
end_color = "#a200fa"
start_color4 = "#01e952"
end_color4 = "#9ffec0"
start_color5 = "#ffffff"
end_color5 = "#878787"
start_color2 = "#fa0000"
end_color2 = "#ffb8b8"

# логотип
logo = """ 
██╗  ██╗██╗██████╗ ██████╗ ███████╗███╗   ██╗ ██████╗ █████╗ ███╗   ███╗███████╗██████╗  █████╗ ██████╗
██║  ██║██║██╔══██╗██╔══██╗██╔════╝████╗  ██║██╔════╝██╔══██╗████╗ ████║██╔════╝██╔══██╗██╔══██╗╚════██╗
███████║██║██║  ██║██║  ██║█████╗  ██╔██╗ ██║██║     ███████║██╔████╔██║█████╗  ██████╔╝███████║  ▄███╔╝
██╔══██║██║██║  ██║██║  ██║██╔══╝  ██║╚██╗██║██║     ██╔══██║██║╚██╔╝██║██╔══╝  ██╔══██╗██╔══██║  ▀▀══╝
██║  ██║██║██████╔╝██████╔╝███████╗██║ ╚████║╚██████╗██║  ██║██║ ╚═╝ ██║███████╗██║  ██║██║  ██║  ██╗
╚═╝  ╚═╝╚═╝╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝ ╚═════╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝  ╚═╝
"""

# ключевые слова, которые могут быть связаны с камерами
camera_keywords = ["camera", "video", "CCTV", "stream", "surveillance", "IPCAM", "DVR"]

# функция для получения диапазона IP-адресов
def get_ip_range():
    gateways = netifaces.gateways()
    print(gradient_text(f"Gateways: {gateways}", start_color5, end_color5))  # отладка

    iface = gateways['default'][netifaces.AF_INET][1]
    ip_info = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]
    ip = ip_info['addr']
    netmask = ip_info['netmask']

    print(gradient_text(f"Using interface: {iface}, IP: {ip}, Netmask: {netmask}", start_color5, end_color5))  # отладка

    # вычисляем начало и конец диапазона IP
    network, subnet = ip.split('.'), netmask.split('.')
    range_start = f"{network[0]}.{network[1]}.{network[2]}.1"
    range_end = f"{network[0]}.{network[1]}.{network[2]}.254"

    return f"{range_start}/{subnet.count('255') * 8}"


# функция для сканирования сети
def scan_network(ip_range):
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    result = srp(packet, timeout=3, verbose=0)[0]

    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})

    return devices


# функция для сканирования портов
def scan_ports(ip, ports):
    open_ports = []
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(2)  # увеличить таймаут для более медленных устройств
        result = sock.connect_ex((ip, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    return open_ports


# функция для проверки камеры
def check_camera_by_http(ip):
    urls = [
        f"http://{ip}:80", f"http://{ip}:443", f"http://{ip}:8080",
        f"http://{ip}:8000", f"http://{ip}:8888", f"http://{ip}:10001"
    ]
    for url in urls:
        try:
            response = requests.get(url, timeout=2)
            response_text = response.text.lower()
            for kw in camera_keywords:
                if kw in response_text:
                    return True
        except requests.exceptions.RequestException:
            continue
    return False
# функция для проверки камеры
def is_camera(ip, open_ports):
    camera_ports = [80, 81, 443, 554, 8080, 8000, 8888, 10001]
    matching_ports = [port for port in open_ports if port in camera_ports]
    is_http_camera = check_camera_by_http(ip)
    return (bool(matching_ports) or is_http_camera), matching_ports

# основная функция для поиска камер
def find_cameras(ip_range):
    devices = scan_network(ip_range)
    cameras = []
    camera_ports = [80, 81, 443, 554, 8080, 8000, 8888, 10001]  # добавлены дополнительные порты

    for device in devices:
        ip = device['ip']
        if ip == '192.168.0.1':  # исключаем роутер или другой известный IP-адрес
            print(gradient_text(f"Пропущен роутер IP: {ip}", start_color5, end_color5))
            continue

        print(gradient_text(f"Проверка IP: {ip}", start_color5, end_color5))
        open_ports = scan_ports(ip, camera_ports)
        print(gradient_text(f"Открытые порты: {open_ports}", start_color5, end_color5))

        is_cam, matching_ports = is_camera(ip, open_ports)
        if is_cam:
            device['open_ports'] = matching_ports
            cameras.append(device)
            print(gradient_text(f"Камера найдена! IP: {ip}, Порты: {matching_ports}", start_color4, end_color4))
        else:
            print(gradient_text(f"Камера не найдена для IP: {ip}", start_color2, end_color2))

    return cameras

if __name__ == "__main__":
    clear_console()
    print(gradient_text(logo, start_color, end_color))  # Печать логотипа с градиентом
    ip_range = get_ip_range()
    print(gradient_text("Сканирование сети...", start_color, end_color))
    cameras = find_cameras(ip_range)

    if cameras:
        print(gradient_text("Найдены камеры:", start_color4, end_color4))
        for camera in cameras:
            print(f"IP: {camera['ip']}, MAC: {camera['mac']}, Open Ports: {camera['open_ports']}")
            input(" ")
    else:
        print(gradient_text("В сети не найдено камер.", start_color2, end_color2))
