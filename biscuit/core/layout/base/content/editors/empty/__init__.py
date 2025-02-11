import tkinter as tk

from .shortcuts import Shortcuts


class Empty(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.base = master.base

        self.bg = "#FFFFFF"
        self.fg = "#787878"
        self.config(bg=self.bg, bd=0, relief=tk.FLAT)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.logo = tk.Label(self, image=self.base.settings.res.logo, bg=self.bg)
        self.logo.grid(row=0, column=0)

        self.shortcuts = Shortcuts(self, bg=self.bg)
        self.shortcuts.grid(row=1, column=0, pady=(0, 40))

        self.shortcuts.add_shortcut("Show all commands", ["Ctrl", "Shift", "p"])
        self.shortcuts.add_shortcut("Toggle terminal", ["Ctrl", "`"])
        self.shortcuts.add_shortcut("Open Folder", ["Ctrl", "Shift", "o"])

        #TODO open new empty file
        self.bind("<Double-Button-1>", lambda _: ...)

    # TODO drop to open
    # def drop(self, event):
    #     if os.path.isfile(event.data):
    #         self.base.open_editor(event.data, exists=True)
    #     elif os.path.isdir(event.data):
    #         self.base.events.open_in_new_window(dir=event.data)
