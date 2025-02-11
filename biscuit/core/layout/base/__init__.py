import tkinter as tk
from tkinter.constants import *

from .content import ContentPane
from .sidebar import Sidebar


class BaseFrame(tk.Frame):
    """
    Main frame holds Sidebar and ContentPane
    .
    App
    └── Root
        ├── Menubar
        ├── BaseFrame
        │    ├── Sidebar
        │    └── ContentPane 
        └── StatusBar
    """
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.base = master.base
        
        self.config(bg="#dfdfdf")

        self.sidebar = Sidebar(self)
        self.contentpane = ContentPane(master=self)

        self.sidebar.pack(side=LEFT, fill=Y)
        self.contentpane.pack(side=LEFT, fill=BOTH, expand=True)
