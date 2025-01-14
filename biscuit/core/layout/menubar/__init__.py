import tkinter as tk

from .item import MenubarItem


class Menubar(tk.Frame):
    """
    Root frame holds Menubar, BaseFrame, and Statusbar
    .
    App
    └── Root
        ├── Menubar
        ├── BaseFrame
        └── Statusbar
    """
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.base = master.base

        self.menus = []

        self.config(bg="#f8f8f8")
        self.events = self.base.events
        self.add_menus()
        
    def add_menu(self, text):
        new_menu = MenubarItem(self, text)
        new_menu.pack(side=tk.LEFT, fill=tk.X, padx=0)
        self.menus.append(new_menu)
        
        return new_menu

    def add_menus(self):
        self.add_file_menu()
        self.add_edit_menu()
        self.add_view_menu()

    # TODO: Implement events for the menu items
    def add_file_menu(self):
        events = self.events

        file_menu = self.add_menu("File")
        file_menu.menu.add_item("New File", events.new_file)
        file_menu.menu.add_item("New Window", events.new_window)
        file_menu.menu.add_separator()
        file_menu.menu.add_item("Open File", events.open_file)
        file_menu.menu.add_item("Open Folder", events.open_directory)
        # TODO open recent files 
        file_menu.menu.add_separator()
        file_menu.menu.add_item("Close Editor", events.close_file)
        file_menu.menu.add_item("Close Folder", events.close_dir)
        file_menu.menu.add_item("Close Window", events.quit)
        file_menu.menu.add_separator()
        file_menu.menu.add_item("Save", events.save)
        file_menu.menu.add_item("Save As...", events.save_as)
        file_menu.menu.add_item("Save All", events.save_all)
        file_menu.menu.add_separator()
        file_menu.menu.add_item("Exit", events.quit)

    def add_edit_menu(self):
        events = self.events

        edit_menu = self.add_menu("Edit")
        edit_menu.menu.add_item("Undo", events.undo)
        edit_menu.menu.add_item("Redo", events.redo)
        edit_menu.menu.add_separator()
        edit_menu.menu.add_item("Cut", events.cut)
        edit_menu.menu.add_item("Copy", events.copy)
        edit_menu.menu.add_item("Paste", events.paste)
        edit_menu.menu.add_separator()
        edit_menu.menu.add_item("Find",)
        edit_menu.menu.add_item("Replace",)
    
    def add_view_menu(self):
        events = self.events

        view_menu = self.add_menu("View")
        view_menu.menu.add_item("Side Bar",)
        view_menu.menu.add_item("Console",)
        view_menu.menu.add_item("Status Bar",)
        view_menu.menu.add_item("Menu",)
        view_menu.menu.add_separator()
        view_menu.menu.add_item("Syntax",)
        view_menu.menu.add_item("Indentation",)
        view_menu.menu.add_item("Line Endings",)

    def close_all_menus(self, event):
        for menu in self.menus:
            menu.hide()

    def show_menu(self, show):
        for i in self.menus:
            if i.name != show.name:
                i.hide()
    
    def hover_file_menu(self, event):
        if self.menudown:
            self.show_menu(self.file_menu)
            self.file_menu.show(event)
    
    def hover_edit_menu(self, event):
        if self.menudown:
            self.show_menu(self.edit_menu)
            self.edit_menu.show(event)
    
    def hover_view_menu(self, event):
        if self.menudown:
            self.show_menu(self.view_menu)
            self.view_menu.show(event)
