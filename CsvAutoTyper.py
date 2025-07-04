import csv
import pyautogui
import tkinter as tk
from tkinter import messagebox
from pynput import keyboard
from arktklib import FileSelector

class CsvAutoTyper:
    def __init__(self, root):
        self.root = root
        self.root.title("Csv Auto Typer")
        self.root.geometry("700x180")
        self.root.resizable(False, False)
        root.attributes('-topmost', True)

        self.is_topmost = tk.BooleanVar(value=True)
        self.processing = False
        self.data = []
        self.current_index = 0

        self.build_gui()

        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def build_gui(self):
        setting_frame = tk.Frame(self.root)
        setting_frame.pack(pady=10)

        self.selector = FileSelector(setting_frame, category="csvファイル", filetypes=[("CSV files", "*.csv")], on_select=self.load_file)
        self.selector.grid(row=0, column=0, padx=20)

        check = tk.Checkbutton(setting_frame, text="常に最前面に表示", variable=self.is_topmost, command=self.toggle_topmost)
        check.grid(row=0, column=1, padx=20)

        nav_frame = tk.Frame(self.root)
        nav_frame.pack(pady=10)

        tk.Label(nav_frame, text="次にタイピング").grid(row=0, column=2)

        self.prev_label = tk.Label(nav_frame, text="", width=14, anchor="center", relief="solid")
        self.prev_label.grid(row=1, column=0)

        self.left_arrow = tk.Label(nav_frame, text="<---F9----")
        self.left_arrow.grid(row=1, column=1)

        self.current_label = tk.Label(nav_frame, text="", width=14, anchor="center", relief="solid")
        self.current_label.grid(row=1, column=2)

        self.right_arrow = tk.Label(nav_frame, text="---F10--->")
        self.right_arrow.grid(row=1, column=3)

        self.next_label = tk.Label(nav_frame, text="", width=14, anchor="center", relief="solid")
        self.next_label.grid(row=1, column=4)

    def toggle_topmost(self):
        is_topmost = self.is_topmost.get()
        root.attributes('-topmost', is_topmost)

    def load_file(self, _):
        file_path = self.selector.get()
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    self.data = [cell for row in reader for cell in row]

                self.current_index = 0
                self.update_info()
                messagebox.showinfo("Success", "ファイルの読み込みに成功しました")  
            except Exception as e:
                messagebox.showerror("Error", f"ファイルの読み込みに失敗しました: {e}")

    def update_info(self):
        if not self.data:
            self.prev_label.config(text="")
            self.current_label.config(text="")
            self.next_label.config(text="")
            return

        if self.current_index >= len(self.data):
            self.current_index = 0

        prev = self.data[self.current_index - 1] if self.current_index > 0 else self.data[-1]
        current = self.data[self.current_index]
        next = self.data[(self.current_index + 1) % len(self.data)]

        self.prev_label.config(text=prev)
        self.current_label.config(text=current)
        self.next_label.config(text=next)

    def type_and_enter(self, text):
        pyautogui.write(text)
        pyautogui.press('enter')

    def type_next_string(self):
        if self.processing:
            return
        self.processing = True
        try:
            if self.current_index < len(self.data):
                self.type_and_enter(self.data[self.current_index])
                self.current_index += 1
            else:
                self.current_index = 0
                self.type_and_enter(self.data[self.current_index])
                self.current_index += 1
        finally:
            self.update_info()
            self.processing = False

    def type_previous_string(self):
        if self.processing:
            return
        self.processing = True
        try:
            if self.current_index > 0:
                self.type_and_enter(self.data[self.current_index])
                self.current_index -= 1
            else:
                self.type_and_enter(self.data[self.current_index])
                self.current_index = len(self.data) - 1
        finally:
            self.update_info()
            self.processing = False

    def on_press(self, key):
        if key == keyboard.Key.f10:
            if self.data == []:
                messagebox.showwarning("Warning", "データがありません。")
                return
            self.type_next_string()
        elif key == keyboard.Key.f9:
            if self.data == []:
                messagebox.showwarning("Warning", "データがありません。")
                return
            self.type_previous_string()


if __name__ == "__main__":
    root = tk.Tk()
    app = CsvAutoTyper(root)
    root.mainloop()
    app.listener.stop()
    app.listener.join()