import subprocess
import customtkinter as ctk
import os
import requests
import sys
import threading
import time
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
from io import BytesIO
from pathlib import Path
import queue
import webbrowser

# Версия лоадера
VERSION = "1.2"
VERSION_URL_TEMPLATE = "https://raw.githubusercontent.com/FileInstaller/LoaderFiles/refs/heads/main/1.1"  # URL для проверки версии в имени файла
LOADER_DOWNLOAD_URL = "https://raw.githubusercontent.com/FileInstaller/LoaderFiles/refs/heads/main/loader_newversion.py"  # URL для скачивания новой версии
image_url = "https://raw.githubusercontent.com/FileInstaller/LoaderFiles/refs/heads/main/изображение_2024-10-20_205140496.png"  # Замените на реальный URL изображения

# Путь для загрузки файлов
DOWNLOAD_PATH = "C:/DeadlySoft/Sources"
if not os.path.exists(DOWNLOAD_PATH):
    os.makedirs(DOWNLOAD_PATH)

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

class LoaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        print("------Loaded DeadlySOFT------")
        print("------------Logs------------")
        self.title("DeadlySoft Loader")
        self.geometry("425x510")
        self.resizable(False, False)
        self.configure(bg="grey20")

        # Инициализация UI элементов
        self.label = ctk.CTkLabel(self, text=" DeadlySoft Loader ", font=("Arial", 16), fg_color="grey20")
        self.label.pack(pady=10)

        self.status_text = ctk.StringVar()
        self.status_label = ctk.CTkLabel(self, textvariable=self.status_text, font=("Arial", 12), fg_color="grey20")
        self.status_label.pack(pady=5)

        # Полоска прогресса загрузки лоадера
        self.loader_progress = ctk.CTkProgressBar(self, width=300)
        self.loader_progress.pack(pady=10)
        self.loader_progress.set(0)

        self.ui_queue = queue.Queue()

        self.after(100, self.process_ui_queue)

        self.check_for_updates()



    def show_progress(self, text):
        self.clear_frame()
        self.status_label = ctk.CTkLabel(self, text=text, font=("Arial", 12), fg_color="grey20")
        self.status_label.pack(pady=10)

    def process_ui_queue(self):
        try:
            while True:
                cmd = self.ui_queue.get_nowait()
                cmd()
        except queue.Empty:
            self.after(100, self.process_ui_queue)

    # метод загрузки и скругления изображения
    def load_ctk_image_from_url(self, url):
        response = requests.get(url)
        image_data = response.content
        original_image = Image.open(BytesIO(image_data))
        image = original_image.resize((100, 100), Image.LANCZOS)  # увеличение размера до 100x100
        # уменьшенное скругление логотипа
        mask = Image.new('L', (100, 100), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([0, 0, 100, 100], radius=20, fill=255)  # меньший радиус скругления

        rounded_image = Image.new('RGBA', (100, 100))
        rounded_image.paste(image, (0, 0), mask=mask)

        return ctk.CTkImage(light_image=rounded_image, dark_image=rounded_image)

    def check_for_updates(self):
        print("checked for updates")
        self.status_text.set("Checking for updates...")
        threading.Thread(target=self._check_and_update).start()

    def _check_and_update(self):
        try:
            self.loader_progress.set(0.5)  # обновление прогресса загрузки лоадера
            # Конструирование URL для текущей версии
            current_version_url = VERSION_URL_TEMPLATE
            response = requests.head(current_version_url)

            if response.status_code == 200:
                # Если версия текущая, пропускаем обновление
                self.status_text.set("Loader is up to date.")
                self.loader_progress.set(1)  # обновление прогресса загрузки лоадера
                self.show_main_menu()
            else:
                # Если версии нет, скачиваем новую
                self.status_text.set("New version found. Downloading...")
                self.loader_progress.set(0.75)  # обновление прогресса загрузки лоадера
                self.download_and_replace(LOADER_DOWNLOAD_URL)
        except Exception as e:
            self.status_text.set(f"Error checking for updates: {e}")
            self.loader_progress.set(1)  # обновление прогресса загрузки лоадера
            self.show_main_menu()

    def download_and_replace(self, url):
        print("Загрузка новой версии и замена текущей!")
        try:
            # отображаем статус в консоли и интерфейсе
            self.status_text.set("Downloading new version...")
            print("Статус: Загрузка новой версии...")
            response = requests.get(url)
            response.raise_for_status()

            # путь к новому файлу
            new_code_path = Path(__file__).with_name("DGSLoader.py")

            # записываем новый код
            with open(new_code_path, "wb") as f:
                f.write(response.content)

            self.status_text.set("Download complete. Updating...")
            print("Статус: Загрузка завершена. Обновление...")

            time.sleep(2)

            # перезапускаем скрипт
            os.execl(sys.executable, sys.executable, str(new_code_path))

        except Exception as e:
            self.status_text.set(f"Error downloading new version: {e}")
            print(f"Ошибка при загрузке новой версии: {e}")
            self.show_main_menu()

    def show_main_menu(self):
        print("MENU STARTED!")
        print(f"VERSION: {VERSION} ")
        self.clear_frame()
        self.label = ctk.CTkLabel(self, text=f" DeadlySoft Menu | V: {VERSION} ", font=("Arial", 16), fg_color="grey20")
        self.label.pack(pady=10)

        # Инициализация UI элементов
        self.label = ctk.CTkLabel(self, text=f" DeadlySoft {VERSION} Dev Access", font=("Arial", 12), text_color="white")
        self.label.pack(side="bottom", pady=10)

        # Создаем фрейм для кнопок
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(side="bottom", pady=10, fill="x", expand=True)

        # Кнопка поддержки
        self.support_button = ctk.CTkButton(self.button_frame, text="Forum",
                                            command=lambda: self.open_url("https://discord.gg/nPEjUH6rn3"), width=20,
                                            height=20)
        self.support_button.pack(side="left", padx=45)

        # Кнопка форума
        self.forum_button = ctk.CTkButton(self.button_frame, text="News",
                                          command=lambda: self.open_url("https://discord.gg/nPEjUH6rn3"), width=20,
                                          height=20)
        self.forum_button.pack(side="left", padx=45)

        # Кнопка выхода
        self.exit_button = ctk.CTkButton(self.button_frame, text="Exit", command=self.quit, width=20, height=20)
        self.exit_button.pack(side="left", padx=45)

        # дополнительные настройки
        self.configure(bg="grey20")
        self.label.configure(anchor="s", width=30, height=30, pady=5, padx=5)

        self.scripts = [
            {"name": "GSP - BETA", "desc": "Telegram Group Spammer", "url": "https://raw.githubusercontent.com/FileInstaller/LoaderFiles/refs/heads/main/tgfarm%20Experiment.py", "logo": "https://raw.githubusercontent.com/FileInstaller/LoaderFiles/refs/heads/main/gsp.png"},
            {"name": "WiFiBruter", "desc": "WiFi Bruter, medium work", "url": "https://raw.githubusercontent.com/FileInstaller/LoaderFiles/refs/heads/main/wifibrut.py", "logo": "https://raw.githubusercontent.com/FileInstaller/LoaderFiles/refs/heads/main/wifib.png"},
            {"name": "HiddenCamera", "desc": "Find cameras in network", "url": "https://raw.githubusercontent.com/FileInstaller/LoaderFiles/refs/heads/main/hiddencamera.py", "logo": "https://raw.githubusercontent.com/FileInstaller/LoaderFiles/refs/heads/main/hd.png"},
            {"name": "WinColorChanger", "desc": "Changes select color", "url": "https://raw.githubusercontent.com/FileInstaller/LoaderFiles/refs/heads/main/windowscolorselect.py", "logo": "https://raw.githubusercontent.com/FileInstaller/LoaderFiles/refs/heads/main/изображение_2024-10-20_205140496.png"},
            {"name": "RTSP Cracker", "desc": "Cracker RTSP with VLC", "url": "https://raw.githubusercontent.com/FileInstaller/LoaderFiles/refs/heads/main/vlccracker.py", "logo": "https://raw.githubusercontent.com/FileInstaller/LoaderFiles/refs/heads/main/Screenshot%202024-10-21%20005013.png"}

        ]

        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=580, height=300)
        self.scrollable_frame.pack(side="top", padx=10, pady=10)

        # Заполняем список скриптов
        for script in self.scripts:
            frame = ctk.CTkFrame(self.scrollable_frame, fg_color="grey20")
            frame.pack(pady=5, padx=10, fill="both")

            logo = self.load_ctk_image_from_url(script["logo"])
            logo_label = ctk.CTkLabel(frame, image=logo, text="", fg_color="grey20")
            logo_label.pack(side="left", padx=1)

            details_frame = ctk.CTkFrame(frame, fg_color="grey20")
            details_frame.pack(side="left", fill="x", expand=True, padx=10)

            script_name = ctk.CTkLabel(details_frame, text=script["name"], font=("Arial", 16), fg_color="grey20")
            script_name.pack(anchor="w")

            script_desc = ctk.CTkLabel(details_frame, text=script["desc"], font=("Arial", 14), fg_color="grey20")
            script_desc.pack(anchor="w")

            run_button = ctk.CTkButton(frame, text="Start",
                                       command=lambda url=script["url"], name=script["name"]: self.run_script(url,
                                                                                                              name))
            run_button.pack(side="right", padx=10)

    # Метод открытия URL
    def open_url(self, url):
        webbrowser.open(url)

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

    def run_script(self, script_url, script_name):
        print("Starting script...")
        self.status_text.set("Checking script...")
        script_path = os.path.join(DOWNLOAD_PATH, script_name)
        script_path = f"{script_path}.py"  # добавление расширения .py

        if os.path.exists(script_path):
            self.status_text.set("Checking and installing required modules...")
            if self.install_missing_modules(script_path):
                self.status_text.set("Modules installed. Restarting the script...")
                self.run_script_from_cmd(script_path)
            else:
                self.status_text.set("Running script...")
                self.run_script_from_cmd(script_path)
        else:
            self.status_text.set("Downloading script...")
            self.download_and_run_script(script_url, script_path)

    def download_and_run_script(self, script_url, script_path):
        print("Downloaded and runned script")
        script_path = f"{script_path}.py"
        threading.Thread(target=self._download_and_run, args=(script_url, script_path)).start()

    def _download_and_run(self, script_url, script_path):
        print("Downloaded and runned script")
        try:
            self.status_text.set("Downloading...")
            self.ui_queue.put(lambda: self.loader_progress.set(0))  # сброс прогресса загрузки скрипта
            response = requests.get(script_url)
            response.raise_for_status()

            with open(script_path, 'wb') as f:
                f.write(response.content)

            self.status_text.set("Saving...")
            self.ui_queue.put(lambda: self.loader_progress.set(0.5))  # обновление прогресса загрузки скрипта
            time.sleep(2)

            self.status_text.set("Checking and installing required modules...")
            if self.install_missing_modules(script_path):
                self.status_text.set("Modules installed. Restarting the script...")
                self.ui_queue.put(lambda: self.loader_progress.set(0.75))  # обновление прогресса загрузки скрипта
                self.run_script_from_cmd(script_path)
            else:
                self.status_text.set("Starting script...")
                self.ui_queue.put(lambda: self.loader_progress.set(1))  # обновление прогресса загрузки скрипта
                self.run_script_from_cmd(script_path)
        except Exception as e:
            self.status_text.set(f"Error downloading script: {e}")
            self.ui_queue.put(lambda: self.loader_progress.set(1))  # обновление прогресса загрузки скрипта
            self.show_main_menu()

    def run_script_from_cmd(self, script_path):
        # Если уже есть запущенный процесс, останавливаем его
        if hasattr(self, 'current_process') and self.current_process:
            self.stop_running_script()

        print("started from CMD")
        clear_console()
        try:
            self.current_process = subprocess.Popen(["python", script_path])
            self.status_text.set("Script started in CMD.")
            clear_console()
            self.ui_queue.put(lambda: self.loader_progress.set(1))  # обновление прогресса запуска скрипта
            self.show_main_menu()
        except Exception as e:
            self.status_text.set(f"Error running script: {e}")
            self.show_main_menu()

    def stop_running_script(self):
        if hasattr(self, 'current_process') and self.current_process:
            self.current_process.terminate()  # останавливаем текущий процесс
            self.current_process.wait()  # ждем, пока процесс завершится
            self.current_process = None  # сбрасываем ссылку на процесс
            self.status_text.set("Previous script terminated.")
            clear_console()
            self.ui_queue.put(lambda: self.loader_progress.set(0))

    def install_missing_modules(self, script_path):
        user_site_packages = os.path.expanduser(r"~\AppData\Roaming\Python\Python310\site-packages")
        sys.path.append(user_site_packages)

        try:
            with open(script_path, 'r') as file:
                lines = file.readlines()

            missing_modules = []
            for line in lines:
                if line.startswith("import") or line.startswith("from"):
                    module = line.split()[1].split('.')[0]
                    try:
                        __import__(module)
                    except ImportError:
                        missing_modules.append(module)

            if missing_modules:
                print(f"Installing missing modules: {', '.join(missing_modules)}")
                subprocess.check_call([sys.executable, "-m", "pip", "install", *missing_modules])
                return True  # Индикатор того, что были установлены новые модули
        except Exception as e:
            print(f"Error installing modules: {e}")

        return False  # Все модули уже были установлены

    def execute_script(self, script_path):
        print("Executed Script")
        try:
            if self.install_missing_modules(script_path):
                print("Restarting script after installing modules...")
                self.execute_script(script_path)  # Перезапуск скрипта после установки модулей
            else:
                os.system(f'python "{script_path}"')
                self.status_text.set("Script started.")
                self.show_main_menu()
        except Exception as e:
            self.status_text.set(f"Error running script: {e}")

if __name__ == "__main__":
    app = LoaderApp()
    app.mainloop()
