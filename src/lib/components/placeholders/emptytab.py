import tkinter as tk
from tkinter import ttk

from .utils.shortcuts import Shortcuts

class EmptyTab(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.base = master.base

        self.bg = "#FFFFFF"
        self.fg = "#787878"
        self.config(bg=self.bg, bd=0, relief=tk.FLAT)

        self.grid_rowconfigure(0, weight=1)
        # self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.logo_img = self.base.settings.resources.logo.subsample(2)
        self.logo = tk.Label(self, image=self.logo_img, bg=self.bg)
        self.logo.grid(row=0, column=0)

        self.shortcuts = Shortcuts(self, bg=self.bg)
        self.shortcuts.grid(row=1, column=0, pady=(0, 40))

        self.shortcuts.add_shortcut("Show all commands", ["Ctrl", "Shift", "P"])
        self.shortcuts.add_shortcut("Toggle terminal", ["Ctrl", "`"])