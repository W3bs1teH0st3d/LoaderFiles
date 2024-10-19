import customtkinter as ctk
import os
import requests
import sys
import threading
import time
from tkinter import messagebox, colorchooser

# Версия лоадера
VERSION = "1.0"
UPDATE_URL = "https://raw.githubusercontent.com/FileInstaller/LoaderFiles/refs/heads/main/loader_version.py"  # Замените на реальный URL

# Путь для загрузки файлов
DOWNLOAD_PATH = "C:/LoaderTest/"

class LoaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("DeadlySoft Loader")
        self.geometry("400x300")
        self.resizable(False, False)

        # Инициализация UI элементов
        self.label = ctk.CTkLabel(self, text="Welcome to DeadlySoft Loader", font=("Arial", 16))
        self.label.pack(pady=10)

        self.status_text = ctk.StringVar()
        self.status_label = ctk.CTkLabel(self, textvariable=self.status_text, font=("Arial", 12))
        self.status_label.pack(pady=5)

        # Новый прелоадер
        self.canvas = ctk.CTkCanvas(self, width=100, height=100, bg="grey20", highlightthickness=0)
        self.canvas.pack(pady=20)

        self.arc = self.canvas.create_arc((5, 5, 45, 45), start=0, extent=330, style="arc", outline="white", width=3)
        self.angle = 0

        self.progress_thread = threading.Thread(target=self.animate_progress)
        self.progress_thread.daemon = True
        self.progress_thread.start()

        self.check_for_updates()

    def animate_progress(self):
        while True:
            self.angle += 5
            self.canvas.coords(self.arc, 5, 5, 45, 45)  # Центрирование дуги
            self.canvas.itemconfig(self.arc, start=self.angle)
            self.canvas.update()
            time.sleep(0.05)

    def check_for_updates(self):
        self.status_text.set("Checking for updates...")
        threading.Thread(target=self._check_and_update).start()

    def _check_and_update(self):
        try:
            response = requests.get(UPDATE_URL)
            response.raise_for_status()
            new_version = response.text.split('=')[1].strip().strip('"')
            if new_version != VERSION:
                self.status_text.set(f"Found new version: {new_version}")
                self.download_and_replace(response.text)
            else:
                self.status_text.set("Loader is up to date.")
                self.show_main_menu()
        except Exception as e:
            self.status_text.set(f"Error checking for updates: {e}")
            self.show_main_menu()


    def download_and_replace(self, new_code):
        try:
            self.status_text.set("Downloading new version...")
            with open(__file__, "w") as f:
                f.write(new_code)
            self.status_text.set("Update complete. Restarting...")
            time.sleep(2)
            os.execl(sys.executable, sys.executable, *sys.argv)
        except Exception as e:
            self.status_text.set(f"Error updating: {e}")
            self.show_main_menu()


    def show_main_menu(self):
        self.clear_frame()
    
        self.label = ctk.CTkLabel(self, text="DeadlySoft Loader", font=("Arial", 16), bg="grey20")
        self.label.pack(pady=10)
    
        self.scripts = [
            {"name": "Script 1", "desc": "Description 1", "url": "https://example.com/script1.py"},
            {"name": "Script 2", "desc": "Description 2", "url": "https://example.com/script2.py"},
            {"name": "Script 3", "desc": "Description 3", "url": "https://example.com/script3.py"}
        ]
    
        for script in self.scripts:
            frame = ctk.CTkFrame(self, bg="grey20")
            frame.pack(pady=5, padx=10, fill="both")
    
            script_name = ctk.CTkLabel(frame, text=script["name"], font=("Arial", 14), bg="grey20")
            script_name.pack(side="left", padx=10)
            script_desc = ctk.CTkLabel(frame, text=script["desc"], font=("Arial", 10), bg="grey20")
            script_desc.pack(side="left", padx=10)
    
            run_button = ctk.CTkButton(frame, text="Run", command=lambda url=script["url"]: self.run_script(url))
            run_button.pack(side="right", padx=10)


def clear_frame(self):
    for widget in self.winfo_children():
        widget.destroy()


def run_script(self, script_url):
    self.status_text.set(f"Downloading script from {script_url}...")
    threading.Thread(target=self._download_and_run, args=(script_url,)).start()


def _download_and_run(self, script_url):
    try:
        script_name = script_url.split('/')[-1]
        script_path = os.path.join(DOWNLOAD_PATH, script_name)
        response = requests.get(script_url)
        response.raise_for_status()
        with open(script_path, 'w') as f:
            f.write(response.text)
        self.status_text.set(f"Running {script_name}...")
        os.system(f'python "{script_path}"')
        self.status_text.set(f"{script_name} started.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run script: {e}")


if __name__ == "__main__":
    if not os.path.exists(DOWNLOAD_PATH):
        os.makedirs(DOWNLOAD_PATH)

    app = LoaderApp()
    app.mainloop()
