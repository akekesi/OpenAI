import io
import shutil
import requests
import customtkinter
from tkinter import *
from PIL import Image
from io import BytesIO
from class_openai_00 import ChatGPT, DALLE

class App(customtkinter.CTk):
    chat_gpt = None
    first_message = True
    image_content = None
    image_default_path = "image_default.png"
    placeholder_role = "Enter the role of AI, e.g. Be a pirate who loves Ben & Jerry's!"
    placeholder_message = "Enter your message"
    placeholder_prompt = "Enter the prompt, e.g. Rubic Cube jewellery in style of Niki de Saint Phalle"
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
    title_app = "OpenAI - Demo"
    size_image_original = (256, 256)
    size_image_logo = (25, 25)
    size_window = (450, 550)
    padx_grid = 10
    pady_grid = 10

    path_api_key = "api.key"    # api.key file, paste your api key there
    with open(path_api_key, "r") as api_key_open:
        api_key = api_key_open.read()

    def __init__(self):
        super().__init__()

        # main window
        self.title(self.title_app)
        self.geometry(f"{self.size_window[0]}x{self.size_window[1]}")
        self.wm_iconbitmap()
        icon_photo_path = self.image_default_path
        icon_photo = PhotoImage(file=icon_photo_path)
        self.iconphoto(False, icon_photo)

        # tabview
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.tabview = customtkinter.CTkTabview(self, command=self.tab_click)
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

        self.entry_role = customtkinter.CTkEntry(self.frame_role, placeholder_text=self.placeholder_role, justify="center")
        self.entry_role.grid(row=0, column=0, sticky="nsew")

        self.textbox = customtkinter.CTkTextbox(self.frame_text, activate_scrollbars=False)
        self.textbox.grid(row=0, column=0, sticky="nsew")

        self.textbox_scrollbar = customtkinter.CTkScrollbar(self.frame_text, command=self.textbox.yview)
        self.textbox_scrollbar.grid(row=0, column=1, sticky="ns")

        self.textbox.configure(yscrollcommand=self.textbox_scrollbar.set)

        self.entry_message = customtkinter.CTkEntry(self.frame_message, placeholder_text=self.placeholder_message)
        self.entry_message.grid(row=0, column=0, sticky="nsew")

        self.button_send_message = customtkinter.CTkButton(self.frame_message, text="Send", width=75, border_width=2, border_color="#565B5E", command=self.send_message)
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

        self.entry_prompt = customtkinter.CTkEntry(self.frame_prompt, placeholder_text=self.placeholder_prompt, justify="center")
        self.entry_prompt.grid(row=0, column=0, sticky="nsew")

        self.image_default = customtkinter.CTkImage(dark_image=Image.open(self.image_default_path),
                                                    size=self.size_image_original)

        self.label_image = customtkinter.CTkLabel(self.frame_image, image=self.image_default, text="", justify="center")
        self.label_image.grid(row=0, column=0, padx=self.padx_grid, pady=self.pady_grid)

        self.button_generate_image = customtkinter.CTkButton(self.frame_generate, text="Generate", border_width=2, border_color="#565B5E", command=self.generate_image)
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

        # resize	
        self.bind("<Configure>", self.resize)

    def tab_click(self):
        print(f"{self.tab_click.__name__} --> {self.tabview.get()}")

    def send_message(self):
        if self.first_message:
            role = self.entry_role.get()
            self.textbox.insert("end", f"Role: {role}\n")
            self.first_message = False
            self.chat_gpt = ChatGPT(api_key=self.api_key, role=role)
        message = self.entry_message.get()
        answer = self.chat_gpt.question(question=message)
        self.textbox.insert("end", f"> {message}\n")
        self.entry_message.delete(0, "end")
        self.textbox.insert("end", f"> {answer}\n")
        print(f"{self.send_message.__name__}")

    def generate_image(self):
        prompt = self.entry_prompt.get()
        dall_e = DALLE(api_key=self.api_key)
        url = dall_e.create(prompt=prompt,
                           n=1,
                           size=f"{self.size_image_original[0]}x{self.size_image_original[1]}")
        self.image_content = requests.get(url).content
        self.image_content_bytes = io.BytesIO(self.image_content)
        image = customtkinter.CTkImage(dark_image=Image.open(self.image_content_bytes),
                                       size=self.size_image_original)
        self.label_image.configure(image=image)
        print(f"{self.generate_image.__name__}")

    def add_doc(self):
        name_doc = self.input_dialog(text="Name of the text file to save the chat as:",
                                     title="Save as")
        if not name_doc:
            return
        path_txt = f"{name_doc}.txt"
        path_png = f"{name_doc}.png"
        self.save_chat(path_txt)
        self.save_image(path_png)
        data = {"chat": path_txt,
                "image": path_png}

        image = self.image_default_path
        if self.image_content:
            image = self.image_content_bytes
        image_doc = customtkinter.CTkImage(dark_image=Image.open(image),
                                           size=self.size_image_logo)

        n = len(self.widgets_docs[0])
        self.widgets_docs[0].append(
            customtkinter.CTkLabel(self.frame_docs_scrollable, image=image_doc, text="", justify="center")
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

    def input_dialog(self, text: str, title: str):
        dialog = customtkinter.CTkInputDialog(text=text, title=title)
        print(f"{self.input_dialog.__name__}")
        return dialog.get_input()

    def save_chat(self, path_txt):
        with open(path_txt, 'w') as f:
            f.write(self.textbox.get(0.0, "end"))
        print(f"{self.save_chat.__name__}")

    def save_image(self, path_png):
        if self.image_content:
            with open(path_png, "wb") as f:
                f.write(self.image_content)
        else:
            shutil.copyfile(self.image_default_path, path_png)
        print(f"{self.save_image.__name__}")

    def resize(self, event) -> None:
        if self.winfo_width() < self.size_window[0]:
            self.geometry(f'{self.size_window[0]}x{self.winfo_height()}')
        if self.winfo_height() < self.size_window[1]:
            self.geometry(f'{self.winfo_width()}x{self.size_window[1]}')
        print(f"{self.resize.__name__}")


if __name__ == "__main__":
    customtkinter.set_appearance_mode("dark")
    app = App()
    app.mainloop()
