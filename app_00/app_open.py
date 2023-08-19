import os
import customtkinter
from tkinter import *


class AppOpenImage(customtkinter.CTkToplevel):
    path_docs = "docs"
    image_default = "image_default.png"
    image_default_path = os.path.join(path_docs, image_default)
    title_app = "OpenAI - Image"
    padx_grid = 10
    pady_grid = 10

    def __init__(self, image, name):
        super().__init__()

        # attributes
        self.attributes("-topmost", True)
        self.title(self.title_app)
        self.wm_iconbitmap()
        icon_photo_path = self.image_default_path
        icon_photo = PhotoImage(file=icon_photo_path)
        self.after(300, lambda: self.iconphoto(False, icon_photo))

        self.frame_image = customtkinter.CTkFrame(self)
        self.frame_image.grid(row=0, column=0, padx=self.padx_grid, pady=self.padx_grid, sticky="nsew")
        self.frame_image.grid_columnconfigure(0, weight=1)
        self.frame_image.grid_rowconfigure(0, weight=1)

        self.label_image = customtkinter.CTkLabel(self, image=image, text="", justify="center")
        self.label_image.grid(row=0, column=0, padx=self.padx_grid, pady=(self.padx_grid, 0))

        self.label_name = customtkinter.CTkLabel(self, text=name, justify="center")
        self.label_name.grid(row=1, column=0, padx=self.padx_grid, pady=0)
