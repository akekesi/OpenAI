import customtkinter
from tkinter import *


class App(customtkinter.CTkFrame):
    tab_names = ["chat",
                 "docs"]
    padx_grid = 10
    pady_grid = 10

    def __init__(self, master):
        super().__init__(master)

        self.tabview = customtkinter.CTkTabview(master, command=self.tab_click)
        self.tabview.grid(row=0, column=0, padx=self.padx_grid, pady=self.pady_grid, sticky="nsew")
        for tab in self.tab_names:
            self.tabview.add(tab)

        # tab-0
        self.tabview.tab(self.tab_names[0]).grid_rowconfigure(0, weight=1)
        self.tabview.tab(self.tab_names[0]).grid_columnconfigure(0, weight=1)

        self.frame_text = customtkinter.CTkFrame(self.tabview.tab(self.tab_names[0]))
        self.frame_text.grid(row=0, column=0, padx=self.padx_grid, pady=(self.pady_grid, 0), sticky="nsew")
        self.frame_text.grid_rowconfigure(0, weight=1)
        self.frame_text.grid_columnconfigure(0, weight=1)

        self.frame_entry = customtkinter.CTkFrame(self.tabview.tab(self.tab_names[0]))
        self.frame_entry.grid(row=1, column=0, padx=self.padx_grid, pady=self.pady_grid, sticky="nsew")
        self.frame_entry.grid_rowconfigure(0, weight=1)
        self.frame_entry.grid_columnconfigure(0, weight=1)
    
        self.textbox = customtkinter.CTkTextbox(self.frame_text, activate_scrollbars=False)
        self.textbox.grid(row=0, column=0, sticky="nsew")

        self.textbox_scrollbar = customtkinter.CTkScrollbar(self.frame_text, command=self.textbox.yview)
        self.textbox_scrollbar.grid(row=0, column=1, sticky="ns")

        self.textbox.configure(yscrollcommand=self.textbox_scrollbar.set)

        self.entry = customtkinter.CTkEntry(self.frame_entry)
        self.entry.grid(row=0, column=0, sticky="nsew")

        self.button_send_message = customtkinter.CTkButton(self.frame_entry, text="Send", width=75, command=self.send_message)
        self.button_send_message.grid(row=0, column=1, sticky="w")

    def tab_click(self):
        print(f"{self.tab_click.__name__} --> {self.tabview.get()}")

    def send_message(self):
        self.textbox.insert("end", f"> {self.entry.get()}\n")
        self.entry.delete(0, "end")
        print(f"{self.send_message.__name__}")


if __name__ == "__main__":
    customtkinter.set_appearance_mode("dark")
    master = customtkinter.CTk()
    master.title("OpenAI - Demo")
    master.geometry("500x350")
    master.wm_iconbitmap()
    icon_photo_path = "icon_photo.png"
    icon_photo = PhotoImage(file=icon_photo_path)
    master.iconphoto(False, icon_photo)
    master.grid_columnconfigure(0, weight=1)
    master.grid_rowconfigure(0, weight=1)

    app = App(master=master)
    app.grid(row=0, column=0, padx=20, pady=20)

    master.mainloop()
