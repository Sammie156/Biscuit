import tkinter as tk


class BaseGame(tk.Frame):
    """
    Base class for games.
    """
    def __init__(self, master, path=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.base = master.base

        self.path = path
        self.filename = None

        self.exists = False
        self.showpath = False
        self.content = None
        self.diff = False
        self.editable = False

        self.__buttons__ = ()

    def reload(self, *_):
        ...    
        
    def save(self, *_):
        ...
