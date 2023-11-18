import os
import customtkinter
from PIL import Image
from tkinter import PhotoImage


class AppOpenAIOpenDoc(customtkinter.CTkToplevel):
    title_ = "OpenAI"
    tab_names = ["logo",
                 "chat"]

    size_window = (350, 380)
    size_image = (256, 256)
    padx_grid = 10
    pady_grid = 10

    path_img = os.path.join(os.path.dirname(__file__), "..", "img")
    path_img_default = os.path.join(path_img, "image_default.png")

    def __init__(self, name, path_chat, path_logo):
        super().__init__()

        self.attributes("-topmost", True)
        self.title(f"{self.title_} - {name}")
        self.geometry(f"{self.size_window[0]}x{self.size_window[1]}")
        self.wm_iconbitmap()
        icon_photo_path = self.path_img_default
        icon_photo = PhotoImage(file=icon_photo_path)
        self.after(200, lambda: self.iconphoto(False, icon_photo))

        image_open = Image.open(path_logo)
        image = customtkinter.CTkImage(dark_image=image_open,
                                       size=self.size_image)
        with open(path_chat, "r") as f:
            text = f.read()

        # tabview
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.tabview = customtkinter.CTkTabview(self)
        self.tabview.grid(row=0, column=0, padx=self.padx_grid, pady=self.pady_grid, sticky="nsew")
        for tab in self.tab_names:
            self.tabview.add(tab)

        # tab-0
        tmp_tab = 0
        self.tabview.tab(self.tab_names[tmp_tab]).grid_rowconfigure(0, weight=1)
        self.tabview.tab(self.tab_names[tmp_tab]).grid_columnconfigure(0, weight=1)

        self.label_image = customtkinter.CTkLabel(self.tabview.tab(self.tab_names[tmp_tab]), image=image, text="", justify="center")
        self.label_image.grid(row=0, column=0, padx=self.padx_grid, pady=self.padx_grid)

        # tab-1
        tmp_tab = 1
        self.tabview.tab(self.tab_names[tmp_tab]).grid_rowconfigure(0, weight=1)
        self.tabview.tab(self.tab_names[tmp_tab]).grid_columnconfigure(0, weight=1)

        self.frame_text = customtkinter.CTkFrame(self.tabview.tab(self.tab_names[tmp_tab]), fg_color="transparent")
        self.frame_text.grid(row=0, column=0, padx=self.padx_grid, pady=self.pady_grid, sticky="nsew")
        self.frame_text.grid_rowconfigure(0, weight=1)
        self.frame_text.grid_columnconfigure(0, weight=1)

        self.textbox = customtkinter.CTkTextbox(self.frame_text, activate_scrollbars=False, state="disabled")
        self.textbox.grid(row=0, column=0, sticky="nsew")

        self.textbox_scrollbar = customtkinter.CTkScrollbar(self.frame_text, command=self.textbox.yview)
        self.textbox_scrollbar.grid(row=0, column=1, sticky="ns")

        self.textbox.configure(yscrollcommand=self.textbox_scrollbar.set)

        self.textbox.configure(state="normal")
        self.textbox.insert(0.0, text)
        self.textbox.configure(state="disabled")

        # bind
        self.bind('<Alt-Right>', self.click_arrow_right)
        self.bind('<Alt-Left>', self.click_arrow_left)
        self.bind("<Configure>", self.resize)

    def click_arrow_right(self, event):
        tab_current = self.tabview.get()
        index_currant = self.tab_names.index(tab_current)
        index_next = min(len(self.tab_names) - 1, index_currant + 1)
        tab_next = self.tab_names[index_next]
        self.tabview.set(tab_next)

    def click_arrow_left(self, event):
        tab_current = self.tabview.get()
        index_currant = self.tab_names.index(tab_current)
        index_next = max(0, index_currant - 1)
        tab_next = self.tab_names[index_next]
        self.tabview.set(tab_next)

    def resize(self, event) -> None:
        if self.winfo_width() < self.size_window[0]:
            self.geometry(f'{self.size_window[0]}x{self.winfo_height()}')
        if self.winfo_height() < self.size_window[1]:
            self.geometry(f'{self.winfo_width()}x{self.size_window[1]}')


if __name__ == "__main__":
    # arguments
    name = "Alien_BMX"
    path_doc = os.path.join(os.path.dirname(__file__), "..", "doc")
    path_chat=os.path.join(path_doc, name, f"{name}.txt")
    path_logo=os.path.join(path_doc, name, f"{name}.png")

    # AppOpenAIOpenDoc
    customtkinter.set_appearance_mode("dark")
    app = AppOpenAIOpenDoc(name=name,
                     path_chat=path_chat,
                     path_logo=path_logo)
    app.mainloop()
