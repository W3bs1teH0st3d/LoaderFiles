import tkinter as tk
from tkinter import colorchooser
import winreg as reg
import os

# Функция для изменения значений в реестре
def modify_registry(path, name, value, value_type=reg.REG_SZ):
    try:
        registry_key = reg.OpenKey(reg.HKEY_CURRENT_USER, path, 0, reg.KEY_WRITE)
        reg.SetValueEx(registry_key, name, 0, value_type, value)
        reg.CloseKey(registry_key)
        print(f"Registry value for {name} modified successfully")
    except WindowsError as e:
        print(f"Failed to modify registry value for {name}: {e}")

# Функция для выбора цвета и изменения соответствующего значения в реестре
def choose_color(color_name):
    color_code = colorchooser.askcolor(title=f"Choose color for {color_name}")
    if color_code:
        color_rgb = color_code[0]  # RGB значения
        color_rgb_str = f"{int(color_rgb[0])} {int(color_rgb[1])} {int(color_rgb[2])}"
        selected_color_labels[color_name].config(text=f"{color_name}: RGB {color_rgb_str}", bg=color_code[1])

        # Пример пути и значения для изменения в реестре
        registry_path = r"Control Panel\Colors"
        value_name = color_name
        new_value = color_rgb_str

        # Изменение значения в реестре
        modify_registry(registry_path, value_name, new_value, reg.REG_SZ)

        # Обновление отображения примера
        if color_name == "Hilight":
            example_box.config(highlightbackground=color_code[1])
            example_text.tag_configure("highlight", background=color_code[1])
        elif color_name == "HotTrackingColor":
            example_box.config(bg=color_code[1])
        elif color_name == "HilightText":
            example_text.tag_configure("highlight", foreground=color_code[1])

# Функция для выхода из системы
def apply_changes():
    os.system("shutdown /l")

# Создание главного окна
root = tk.Tk()
root.title("Choose color | @Ewinnery | Simples .py!")

# Настройка горизонтального макета
root.geometry("600x400")
# Словарь для хранения меток выбранных цветов
selected_color_labels = {}

# Цвета для выбора
colors = ["Hilight", "HilightText", "HotTrackingColor"]

# Создание фреймов для кнопок и примера
button_frame = tk.Frame(root)
button_frame.pack(side=tk.LEFT, padx=20, pady=20)

example_frame = tk.Frame(root, bd=1, relief=tk.SUNKEN)
example_frame.pack(side=tk.LEFT, padx=20, pady=20)

# Создание кнопок и меток для каждого цвета
for color in colors:
    button = tk.Button(button_frame, text=f"Choose {color} Color", command=lambda c=color: choose_color(c))
    button.pack(pady=10)

    label = tk.Label(button_frame, text=f"{color}:", width=40, height=2)
    label.pack(pady=5)
    selected_color_labels[color] = label

# Создание примера квадрата и текста
example_box = tk.Canvas(example_frame, width=200, height=200, highlightthickness=5, bg="white")
example_box.pack(pady=10)

example_text = tk.Text(example_frame, width=30, height=5)
example_text.pack()
example_text.insert(tk.END, "ABCDFG 123456 -_=+ []{}() <> , . !@#$%^&*() HELLO WORLD, РУССКИЙ ТЕКСТ", "highlight")
example_text.tag_add("highlight", "1.0", "1.end")

# Добавление кнопки 'Apply'
apply_button = tk.Button(button_frame, text="Apply (logout)", command=apply_changes)
apply_button.pack(pady=20)

# Запуск главного цикла
root.mainloop()
