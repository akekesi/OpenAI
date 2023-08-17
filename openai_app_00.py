import requests
import customtkinter
from tkinter import *
from PIL import Image


class App(customtkinter.CTkFrame):
    first_message = True
    tab_names = ["chat",
                 "image",
                 "docs"]
    widgets_docs = [[],     # image of doc: 	widget - Label
                    [],     # name of doc:	    widget - Entry
                    [],     # type of doc:	    widget - Combobox
                    [],     # delete button:    widget - Button
                    []]     # data of doc:      dictionary
    types_docs = ["private",
                  "unlisted",
                  "public"]
    padx_grid = 10
    pady_grid = 10

    def __init__(self, master):
        super().__init__(master)

        self.tabview = customtkinter.CTkTabview(master, command=self.tab_click)
        self.tabview.grid(row=0, column=0, padx=self.padx_grid, pady=self.pady_grid, sticky="nsew")
        for tab in self.tab_names:
            self.tabview.add(tab)

        # tab-0
        self.tabview.tab(self.tab_names[0]).grid_columnconfigure(0, weight=1)
        self.tabview.tab(self.tab_names[0]).grid_rowconfigure(1, weight=1)

        self.frame_role = customtkinter.CTkFrame(self.tabview.tab(self.tab_names[0]))
        self.frame_role.grid(row=0, column=0, padx=self.padx_grid, pady=(self.pady_grid, 0), sticky="nsew")
        self.frame_role.grid_columnconfigure(0, weight=1)

        self.frame_text = customtkinter.CTkFrame(self.tabview.tab(self.tab_names[0]), fg_color="transparent")
        self.frame_text.grid(row=1, column=0, padx=self.padx_grid, pady=(self.pady_grid, 0), sticky="nsew")
        self.frame_text.grid_columnconfigure(0, weight=1)
        self.frame_text.grid_rowconfigure(0, weight=1)

        self.frame_message = customtkinter.CTkFrame(self.tabview.tab(self.tab_names[0]), fg_color="transparent")
        self.frame_message.grid(row=2, column=0, padx=self.padx_grid, pady=self.pady_grid, sticky="nsew")
        self.frame_message.grid_columnconfigure(0, weight=1)

        self.entry_role = customtkinter.CTkEntry(self.frame_role, placeholder_text="Enter the role of AI, e.g. Be a pirate who loves Ben & Jerry's!", justify="center")
        self.entry_role.grid(row=0, column=0, sticky="nsew")

        self.textbox = customtkinter.CTkTextbox(self.frame_text, activate_scrollbars=False)
        self.textbox.grid(row=0, column=0, sticky="nsew")

        self.textbox_scrollbar = customtkinter.CTkScrollbar(self.frame_text, command=self.textbox.yview)
        self.textbox_scrollbar.grid(row=0, column=1, sticky="ns")

        self.textbox.configure(yscrollcommand=self.textbox_scrollbar.set)

        self.entry_message = customtkinter.CTkEntry(self.frame_message, placeholder_text="Enter your message")
        self.entry_message.grid(row=0, column=0, sticky="nsew")

        self.button_send_message = customtkinter.CTkButton(self.frame_message, text="Send", width=75, border_width=2, border_color="#565B5E", command=self.send_message) # disabled unless role filled
        self.button_send_message.grid(row=0, column=1, padx=(self.padx_grid, 0), sticky="e")

        # tab-1
        self.tabview.tab(self.tab_names[1]).grid_columnconfigure(0, weight=1)
        self.tabview.tab(self.tab_names[1]).grid_rowconfigure(1, weight=1)

        self.frame_prompt = customtkinter.CTkFrame(self.tabview.tab(self.tab_names[1]))
        self.frame_prompt.grid(row=0, column=0, padx=self.padx_grid, pady=(self.pady_grid, 0), sticky="nsew")
        self.frame_prompt.grid_columnconfigure(0, weight=1)

        self.frame_image = customtkinter.CTkFrame(self.tabview.tab(self.tab_names[1]))
        self.frame_image.grid(row=1, column=0, padx=self.padx_grid, pady=(self.pady_grid, 0), sticky="nsew")
        self.frame_image.grid_columnconfigure(0, weight=1)
        self.frame_image.grid_rowconfigure(0, weight=1)

        self.frame_generate = customtkinter.CTkFrame(self.tabview.tab(self.tab_names[1]))
        self.frame_generate.grid(row=3, column=0, padx=self.padx_grid, pady=self.pady_grid, sticky="nsew")
        self.frame_generate.grid_columnconfigure(0, weight=1)

        self.entry_prompt = customtkinter.CTkEntry(self.frame_prompt, placeholder_text="Enter the prompt, e.g. Rubic Cube jewellery in style of Niki de Saint Phalle", justify="center")
        self.entry_prompt.grid(row=0, column=0, sticky="nsew")

        self.image_default = customtkinter.CTkImage(light_image=Image.open("image_default.png"),
                                          dark_image=Image.open("image_default.png"),
                                          size=(256, 256))

        self.label_image = customtkinter.CTkLabel(self.frame_image, image=self.image_default, text="", justify="center")
        self.label_image.grid(row=0, column=0, padx=self.padx_grid, pady=self.pady_grid)

        self.button_generate_image = customtkinter.CTkButton(self.frame_generate, text="Generate", border_width=2, border_color="#565B5E", command=self.generate_image) # disabled unless role filled
        self.button_generate_image.grid(row=0, column=0, sticky="nsew")

        # tab-2
        self.tabview.tab(self.tab_names[2]).grid_columnconfigure(0, weight=1)
        self.tabview.tab(self.tab_names[2]).grid_rowconfigure(0, weight=1)

        self.frame_docs = customtkinter.CTkFrame(self.tabview.tab(self.tab_names[2]))
        self.frame_docs.grid(row=0, column=0, padx=self.padx_grid, pady=(self.pady_grid, 0), sticky="nsew")
        self.frame_docs.grid_columnconfigure(0, weight=1)
        self.frame_docs.grid_rowconfigure(0, weight=1)

        self.frame_add_doc = customtkinter.CTkFrame(self.tabview.tab(self.tab_names[2]), fg_color="transparent")
        self.frame_add_doc.grid(row=1, column=0, padx=self.padx_grid, pady=self.pady_grid, sticky="nsew")
        self.frame_add_doc.grid_columnconfigure(0, weight=1)

        self.frame_docs_scrollable = customtkinter.CTkScrollableFrame(self.frame_docs)
        self.frame_docs_scrollable.grid(row=0, column=0, sticky="nsew")
        self.frame_docs_scrollable.grid_columnconfigure(1, weight=1)

        self.button_add_part = customtkinter.CTkButton(self.frame_add_doc, text="Add Doc", width=75, border_width=2, border_color="#565B5E", command=self.add_doc)
        self.button_add_part.grid(row=1, column=0, padx=(0, 2*self.padx_grid+6), pady=0, sticky="e")

    def tab_click(self):
        print(f"{self.tab_click.__name__} --> {self.tabview.get()}")

    def send_message(self):
        if self.first_message:
            self.textbox.insert("end", f"Role: {self.entry_role.get()}\n")
            self.first_message = False
        self.textbox.insert("end", f"> {self.entry_message.get()}\n")
        self.entry_message.delete(0, "end")
        answer = "AI's answer"
        self.textbox.insert("end", f"> {answer}\n")
        print(f"{self.send_message.__name__}")

    def generate_image(self):
        print(f"{self.generate_image.__name__}")

    def add_doc(self):
        name_doc = self.input_dialog(text="Name of the text file to save the chat as:",
                                     title="Save as")
        if not name_doc:
            return
        # check: already exist
        path_txt = f"{name_doc}.txt"
        path_png = f"{name_doc}.png"
        self.save_chat(path_txt)
        self.save_image(path_png)
        data = {"chat": path_txt,
                "image": path_png}
        self.image_doc = customtkinter.CTkImage(light_image=Image.open("image_default.png"),
                                                dark_image=Image.open("image_default.png"),
                                                size=(25, 25))
        n = len(self.widgets_docs[0])
        self.widgets_docs[0].append(
            customtkinter.CTkLabel(self.frame_docs_scrollable, image=self.image_doc, text="", justify="center")
        )
        self.widgets_docs[1].append(
            customtkinter.CTkEntry(self.frame_docs_scrollable)
        )
        self.widgets_docs[2].append(
            customtkinter.CTkComboBox(self.frame_docs_scrollable, values=self.types_docs, width=100, justify="c", state="readonly")
        )
        self.widgets_docs[3].append(
            customtkinter.CTkButton(self.frame_docs_scrollable, text="Delete", width=75, border_width=2, border_color="#565B5E", command=lambda n=n: self.delete_doc(n))
        )
        self.widgets_docs[-1].append(data)
        self.widgets_docs[0][n].grid(row=n, column=0, padx=(0, 0), pady=(self.pady_grid, 0), sticky="ew")
        self.widgets_docs[1][n].grid(row=n, column=1, padx=(self.padx_grid, 0), pady=(self.pady_grid, 0), sticky="ew")
        self.widgets_docs[1][n].configure(state="normal")
        self.widgets_docs[1][n].delete(0, "end")
        self.widgets_docs[1][n].insert(0, name_doc) 
        self.widgets_docs[1][n].configure(state="disabled")
        self.widgets_docs[2][n].grid(row=n, column=2, padx=(self.padx_grid, 0), pady=(self.pady_grid, 0), sticky="ew")
        self.widgets_docs[2][n].set(self.types_docs[0])
        self.widgets_docs[3][n].grid(row=n, column=3, padx=self.padx_grid, pady=(self.pady_grid, 0), sticky="ew")
        print(f"{self.add_doc.__name__}")

    def delete_doc(self, n):
        if self.widgets_docs[0][n]:
            self.widgets_docs[0][n].destroy()
            self.widgets_docs[1][n].destroy()
            self.widgets_docs[2][n].destroy()
            self.widgets_docs[3][n].destroy()
            self.widgets_docs[0][n] = ""
            self.widgets_docs[1][n] = ""
            self.widgets_docs[2][n] = ""
            self.widgets_docs[3][n] = ""
            self.widgets_docs[-1][n] = ""
        print(f"{self.delete_doc.__name__}")

    def save_chat(self, path_txt):
        with open(path_txt, 'w') as f:
            f.write(self.textbox.get(0.0, "end"))
        print(f"{self.save_chat.__name__}")

    def save_image(self, path_png):
        url = "https://www.pngkit.com/png/detail/246-2461405_bojack-horsemann-bojack-horseman-bojack.png"
        response = requests.get(url)
        with open(path_png, "wb") as f:
            f.write(response.content)
        print(f"{self.save_image.__name__}")

    def input_dialog(self, text: str, title: str):
        dialog = customtkinter.CTkInputDialog(text=text, title=title)
        return dialog.get_input()


if __name__ == "__main__":
    customtkinter.set_appearance_mode("dark")
    master = customtkinter.CTk()
    master.title("OpenAI - Demo")
    master.geometry("400x500")
    master.wm_iconbitmap()
    icon_photo_path = "icon_photo.png"
    icon_photo = PhotoImage(file=icon_photo_path)
    master.iconphoto(False, icon_photo)
    master.grid_columnconfigure(0, weight=1)
    master.grid_rowconfigure(0, weight=1)

    app = App(master=master)
    app.grid(row=0, column=0, padx=20, pady=20)

    master.mainloop()
