import io
import os
import json
import shutil
import requests
import customtkinter
from tkinter import *
from PIL import Image
from app_sub_open_doc import AppSubOpenDoc
from class_openai import ChatGPT, DALLE


class AppOpenAI(customtkinter.CTk):
    chat_gpt = None
    first_message = True

    path_git_docs = "docs"
    path_git_assets = "assets"

    name_docs = "00_docs.json"
    name_image_default = "image_default.png"

    path_docs = os.path.join(os.path.dirname(__file__), path_git_docs, name_docs)
    with open(path_docs, 'r') as f:
        docs_data = json.load(f)

    path_image_default = os.path.join(os.path.dirname(__file__), path_git_assets, name_image_default)
    image_generated_content = None
    image_generated_bytes = None

    placeholder_role = "Enter the role of AI, e.g. Be a pirate who loves Ben & Jerry's!"
    placeholder_message = "Enter your message"
    placeholder_prompt = "Enter the prompt, e.g. Pirate with Ben & Jerry's in style of flat art"

    title_app = "OpenAI - Demo"
    tab_names = ["chat",
                 "logo",
                 "docs"]
    widgets_docs = [[],     # image of doc: 	widget - Label
                    [],     # name of doc:	    widget - Entry
                    [],     # type of doc:	    widget - Combobox
                    [],     # delete button:    widget - Button
                    []]     # hash of doc
    types_docs = ["private",
                  "unlisted",
                  "public"]

    size_image_original = (256, 256)
    size_image_logo = (25, 25)
    size_window = (450, 550)

    padx_grid = 10
    pady_grid = 10
    padx_grid_scroll = 16

    path_api_key = os.path.join(os.path.dirname(__file__), "api.key")    # api.key file, paste your api key there
    with open(path_api_key, "r") as api_key_open:
        api_key = api_key_open.read()

    def __init__(self):
        super().__init__()

        # main window
        self.title(self.title_app)
        self.geometry(f"{self.size_window[0]}x{self.size_window[1]}")
        self.wm_iconbitmap()
        icon_photo_path = self.path_image_default
        icon_photo = PhotoImage(file=icon_photo_path)
        self.iconphoto(False, icon_photo)

        # tabview
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.tabview = customtkinter.CTkTabview(self)
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
        self.textbox.grid(row=0, column=0, padx=(self.padx_grid_scroll, 0), sticky="nsew")

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

        image = customtkinter.CTkImage(dark_image=Image.open(self.path_image_default),
                                       size=self.size_image_original)

        self.label_image = customtkinter.CTkLabel(self.frame_image, image=image, text="", justify="center")
        self.label_image.grid(row=0, column=0, padx=self.padx_grid, pady=self.pady_grid)

        self.button_generate_image = customtkinter.CTkButton(self.frame_generate, text="Generate", border_width=2, border_color="#565B5E", command=self.generate_image)
        self.button_generate_image.grid(row=0, column=0, sticky="nsew")

        # tab-2
        self.tabview.tab(self.tab_names[2]).grid_columnconfigure(0, weight=1)
        self.tabview.tab(self.tab_names[2]).grid_rowconfigure(0, weight=1)

        self.frame_docs = customtkinter.CTkFrame(self.tabview.tab(self.tab_names[2]), fg_color="transparent")
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

        # load docs
        self.load_docs()

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
        self.textbox.see("end")

    def generate_image(self):
        prompt = self.entry_prompt.get()
        dall_e = DALLE(api_key=self.api_key)
        url = dall_e.create(prompt=prompt,
                            n=1,
                            size=f"{self.size_image_original[0]}x{self.size_image_original[1]}")
        self.image_generated_content = requests.get(url).content
        self.image_generated_bytes = io.BytesIO(self.image_generated_content)
        image_generated = customtkinter.CTkImage(dark_image=Image.open(self.image_generated_bytes),
                                                 size=self.size_image_original)
        self.label_image.configure(image=image_generated)

    def add_doc(self, doc={}):
        if doc:
            hash = doc["hash"]
            name = doc["name"]
            type = doc["type"]
            image_to_open = os.path.join(os.path.dirname(__file__), self.path_git_docs, doc["logo"])
        else:
            hash = str(len(self.docs_data) + 1)
            name = self.input_dialog(text="Enter the name of the doc:",
                                     title="Name of Doc")
            type = 0
            if not name:
                return
            name_txt = f"{name}.txt"
            name_png = f"{name}.png"
            self.save_chat(name_txt)
            if self.image_generated_bytes:
                self.save_image(name_png)
                image_to_open = self.image_generated_bytes
            else:
                image_to_open = os.path.join(os.path.dirname(__file__), self.path_git_docs, name_png)
                shutil.copyfile(self.path_image_default, image_to_open)
            data = {hash: {"state": 1,
                           "hash": hash,
                           "name": name,
                           "chat": name_txt,
                           "logo": name_png,
                           "type": 1}}
            self.docs_data.update(data)
            self.update_docs()
            doc = data[hash]
        image_doc = customtkinter.CTkImage(dark_image=Image.open(image_to_open),
                                           size=self.size_image_logo)
        n = len(self.widgets_docs[0])
        self.widgets_docs[0].append(
            customtkinter.CTkLabel(self.frame_docs_scrollable, image=image_doc, text="", justify="center", cursor="hand2")
        )
        self.widgets_docs[1].append(
            customtkinter.CTkEntry(self.frame_docs_scrollable)
        )
        self.widgets_docs[2].append(
            customtkinter.CTkComboBox(self.frame_docs_scrollable, values=self.types_docs, width=100, justify="c", state="readonly", command=lambda type=type, n=n: self.update_type(type, n))
        )
        self.widgets_docs[3].append(
            customtkinter.CTkButton(self.frame_docs_scrollable, text="Delete", width=75, border_width=2, border_color="#565B5E", command=lambda n=n: self.delete_doc(n))
        )
        self.widgets_docs[-1].append(hash)
        self.widgets_docs[0][n].grid(row=n, column=0, padx=(0, 0), pady=(self.pady_grid, 0), sticky="ew")
        self.widgets_docs[0][n].bind("<Button-1>", lambda event, name=doc["name"], path_chat=os.path.join(os.path.dirname(__file__), self.path_git_docs, doc["chat"]), path_logo=os.path.join(os.path.dirname(__file__), self.path_git_docs, doc["logo"]): self.open_doc(name, path_chat, path_logo))
        self.widgets_docs[1][n].grid(row=n, column=1, padx=(self.padx_grid, 0), pady=(self.pady_grid, 0), sticky="ew")
        self.widgets_docs[1][n].configure(state="normal")
        self.widgets_docs[1][n].delete(0, "end")
        self.widgets_docs[1][n].insert(0, name) 
        self.widgets_docs[1][n].configure(state="disabled")
        self.widgets_docs[2][n].grid(row=n, column=2, padx=(self.padx_grid, 0), pady=(self.pady_grid, 0), sticky="ew")
        self.widgets_docs[2][n].set(self.types_docs[type])
        self.widgets_docs[3][n].grid(row=n, column=3, padx=self.padx_grid, pady=(self.pady_grid, 0), sticky="ew")

    def delete_doc(self, n):
        hash = self.widgets_docs[-1][n]
        self.docs_data[hash]["state"] = 0 
        self.update_docs()
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

    def input_dialog(self, text: str, title: str):
        dialog = customtkinter.CTkInputDialog(text=text, title=title)
        return dialog.get_input()

    def save_chat(self, name_txt):
        path_txt = os.path.join(os.path.dirname(__file__), self.path_git_docs, name_txt)
        with open(path_txt, 'w') as f:
            f.write(self.textbox.get(0.0, "end"))

    def save_image(self, name_png):
        path_png = os.path.join(os.path.dirname(__file__), self.path_git_docs, name_png)
        with open(path_png, "wb") as f:
            f.write(self.image_generated_content)

    def load_docs(self):
        for doc in self.docs_data.values():
            if doc["state"]:
                self.add_doc(doc)

    def update_docs(self):
        with open(self.path_docs, "w") as f:
            json.dump(self.docs_data, f, indent=4)

    def update_type(self, type, n):
        hash = self.widgets_docs[-1][n]
        self.docs_data[hash]["type"] = self.types_docs.index(type) 
        self.update_docs()

    def open_doc(self, name, path_chat, path_logo):
        AppSubOpenDoc(name=name,
                   path_chat=path_chat,
                   path_logo=path_logo)

    def resize(self, event) -> None:
        if self.winfo_width() < self.size_window[0]:
            self.geometry(f'{self.size_window[0]}x{self.winfo_height()}')
        if self.winfo_height() < self.size_window[1]:
            self.geometry(f'{self.winfo_width()}x{self.size_window[1]}')


if __name__ == "__main__":
    # AppOpenAI()
    customtkinter.set_appearance_mode("dark")
    app = AppOpenAI()
    app.mainloop()
