import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import sympy as sp
import tkinter as tk

class AdvancedCalculator(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, padding=10, **kwargs)
        self.pack(fill=BOTH, expand=YES)
        self.digitsvar = ttk.StringVar(value="0")
        self.is_day = True

        self.create_num_display()
        self.create_num_pad()
        self.create_theme_toggle()

    def create_num_display(self):
        container = ttk.Frame(master=self, padding=2)
        container.pack(fill=X, pady=20)
        digits = ttk.Label(
            master=container,
            font="TkFixedFont 14",
            textvariable=self.digitsvar,
            anchor=E,
            bootstyle="primary"
        )
        digits.pack(fill=X)

    def create_num_pad(self):
        container = ttk.Frame(master=self, padding=2)
        container.pack(fill=BOTH, expand=YES)
        matrix = [
            ("%", "C", "CE", "/"),
            (7, 8, 9, "*"),
            (4, 5, 6, "-"),
            (1, 2, 3, "+"),
            ("±", 0, ".", "="),
        ]
        for i, row in enumerate(matrix):
            for j, char in enumerate(row):
                button = ttk.Button(
                    master=container,
                    text=char,
                    command=lambda char=char: self.on_button_click(char),
                    bootstyle="secondary" if isinstance(char, str) else "primary"
                )
                button.grid(row=i, column=j, sticky=NSEW, padx=2, pady=2)
        for i in range(4):
            container.grid_columnconfigure(i, weight=1)
            container.grid_rowconfigure(i, weight=1)

    def create_theme_toggle(self):
        toggle_frame = ttk.Frame(master=self, padding=2)
        toggle_frame.pack(fill=X, pady=10)
        self.toggle_button = ttk.Button(
            master=toggle_frame,
            text="Switch to Night Mode",
            command=self.toggle_theme,
            bootstyle="info"
        )
        self.toggle_button.pack(fill=X)

    def toggle_theme(self):
        if self.is_day:
            self.master.style.theme_use("darkly")
            self.toggle_button.config(text="Switch to Day Mode")
        else:
            self.master.style.theme_use("flatly")
            self.toggle_button.config(text="Switch to Night Mode")
        self.is_day = not self.is_day

    def on_button_click(self, char):
        if char == "=":
            try:
                expression = self.digitsvar.get()
                result = sp.sympify(expression)
                self.digitsvar.set(result)
            except Exception as e:
                self.digitsvar.set("Error")
        elif char == "C":
            self.digitsvar.set("0")
        elif char == "CE":
            current_text = self.digitsvar.get()
            self.digitsvar.set(current_text[:-1] if len(current_text) > 1 else "0")
        elif char == "±":
            current_text = self.digitsvar.get()
            if current_text.startswith("-"):
                self.digitsvar.set(current_text[1:])
            else:
                self.digitsvar.set(f"-{current_text}")
        else:
            current_text = self.digitsvar.get()
            if current_text == "0":
                self.digitsvar.set(str(char))
            else:
                self.digitsvar.set(current_text + str(char))

if __name__ == "__main__":
    app = ttk.Window(
        title="Advanced Calculator",
        themename="flatly",
        size=(350, 450),
        resizable=(False, False),
    )
    AdvancedCalculator(app)
    app.mainloop()
