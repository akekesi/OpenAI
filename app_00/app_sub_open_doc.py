import os
import customtkinter
from tkinter import *
from PIL import Image


class AppSubOpenDoc(customtkinter.CTkToplevel):
    path_git_assets = "assets"
    name_image_default = "image_default.png"
    path_image_default = os.path.join(os.path.dirname(__file__), path_git_assets, name_image_default)

    title_prefix = "OpenAI"
    tab_names = ["logo",
                 "chat"]

    size_image_original = (256, 256)
    size_window = (350, 380)

    padx_grid = 10
    pady_grid = 10
    padx_grid_scroll = 16

    def __init__(self, name, path_chat, path_logo):
        super().__init__()

        # attributes
        image_open = Image.open(path_logo)
        image = customtkinter.CTkImage(dark_image=image_open,
                                       size=self.size_image_original)
        with open(path_chat, "r") as f:
            text = f.read()

        self.attributes("-topmost", True)
        self.title(f"{self.title_prefix} - {name}")
        self.geometry(f"{self.size_window[0]}x{self.size_window[1]}")
        self.wm_iconbitmap()
        icon_photo_path = self.path_image_default
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
        self.textbox.grid(row=0, column=0, padx=(self.padx_grid_scroll, 0), sticky="nsew")

        self.textbox_scrollbar = customtkinter.CTkScrollbar(self.tabview.tab(self.tab_names[1]), command=self.textbox.yview)
        self.textbox_scrollbar.grid(row=0, column=1, sticky="ns")

        self.textbox.configure(yscrollcommand=self.textbox_scrollbar.set)
        self.textbox.insert(0.0, text)
        self.textbox.configure(state="disabled")

        # resize
        self.bind("<Configure>", self.resize)

    def resize(self, event) -> None:
        if self.winfo_width() < self.size_window[0]:
            self.geometry(f'{self.size_window[0]}x{self.winfo_height()}')
        if self.winfo_height() < self.size_window[1]:
            self.geometry(f'{self.winfo_width()}x{self.size_window[1]}')


if __name__ == "__main__":
    # arguments for AppSubOpenDoc()
    path_git_docs = "docs"
    name = "bart_movie"
    name_txt = f"{name}.txt"
    name_png = f"{name}.png"
    path_chat = os.path.join(os.path.join(os.path.dirname(__file__), path_git_docs, name_txt))
    path_logo = os.path.join(os.path.join(os.path.dirname(__file__), path_git_docs, name_png))

    # AppSubOpenDoc()
    customtkinter.set_appearance_mode("dark")
    app = AppSubOpenDoc(name=name,
                     path_chat=path_chat,
                     path_logo=path_logo)
    app.mainloop()
