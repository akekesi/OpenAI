import os
import customtkinter
from tkinter import *


class AppOpenDoc(customtkinter.CTkToplevel):
    path_assets = "assets"
    image_default = "image_default.png"
    image_default_path = os.path.join(path_assets, image_default)
    tab_names = ["logo",
                 "chat"]
    title_app = "OpenAI - "

    size_window = (350, 380)

    padx_grid = 10
    pady_grid = 10

    def __init__(self, image, text, name):
        super().__init__()

        # attributes
        self.attributes("-topmost", True)
        self.title(f"{self.title_app}{name}")
        self.geometry(f"{self.size_window[0]}x{self.size_window[1]}")
        self.wm_iconbitmap()
        icon_photo_path = self.image_default_path
        icon_photo = PhotoImage(file=icon_photo_path)
        self.after(300, lambda: self.iconphoto(False, icon_photo))

        # tabview
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.tabview = customtkinter.CTkTabview(self)
        self.tabview.grid(row=0, column=0, padx=self.padx_grid, pady=self.pady_grid, sticky="nsew")
        for tab in self.tab_names:
            self.tabview.add(tab)

        # tab-0
        self.tabview.tab(self.tab_names[0]).grid_columnconfigure(0, weight=1)
        self.tabview.tab(self.tab_names[0]).grid_rowconfigure(0, weight=1)
        self.label_image = customtkinter.CTkLabel(self.tabview.tab(self.tab_names[0]), image=image, text="", justify="center")
        self.label_image.grid(row=0, column=0, padx=self.padx_grid, pady=self.padx_grid)

        # tab-1
        self.tabview.tab(self.tab_names[1]).grid_columnconfigure(0, weight=1)
        self.tabview.tab(self.tab_names[1]).grid_rowconfigure(0, weight=1)
        self.textbox = customtkinter.CTkTextbox(self.tabview.tab(self.tab_names[1]), activate_scrollbars=False)
        self.textbox.grid(row=0, column=0, sticky="nsew")

        self.textbox_scrollbar = customtkinter.CTkScrollbar(self.tabview.tab(self.tab_names[1]), command=self.textbox.yview)
        self.textbox_scrollbar.grid(row=0, column=1, sticky="ns")

        self.textbox.configure(yscrollcommand=self.textbox_scrollbar.set)
        self.textbox.insert(0.0, text)
        self.textbox.configure(state="disabled")

        print(self.tabview.tab("logo").winfo_height())
        print(self.tabview.tab("logo").winfo_width())
        print(self.winfo_height())
        print(self.winfo_width())

        # resize
        self.bind("<Configure>", self.resize)

    def resize(self, event) -> None:
        if self.winfo_width() < self.size_window[0]:
            self.geometry(f'{self.size_window[0]}x{self.winfo_height()}')
        if self.winfo_height() < self.size_window[1]:
            self.geometry(f'{self.winfo_width()}x{self.size_window[1]}')