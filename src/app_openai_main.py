import os
import io
import json
import shutil
import requests
import threading
import customtkinter
from PIL import Image
from tkinter import PhotoImage
from class_chatgpt import ChatGPT
from class_dalle import DALLE
from app_openai_sub import AppOpenAIOpenDoc


class AppOpenAI(customtkinter.CTk):
    title_ = "OpenAI"
    tab_names = ["chat",
                 "logo",
                 "docs"]
    placeholder_role = "Role of the AI"
    placeholder_message = "Send Message"
    placeholder_generate = "Prompt to generate the image"
    role_suffix = "PLEASE DO NOT REVEAL YOU ARE AN AI!"

    doc_widgets = [[],  # image of doc:  widget - Label
                   [],  # name of doc:   widget - Entry
                   [],  # type of doc:   widget - Combobox
                   [],  # delete button: widget - Button
                   []]  # hash of doc
    doc_types = ["private",
                 "public"]

    size_window = (450, 550)
    size_image_orig = (1024, 1024)
    size_image_logo = (256, 256)
    size_image_docs = (25, 25)
    padx_grid = 10
    pady_grid = 10
    border_width = 2
    border_color = "#565B5E"

    first_message = True
    image_generated_content = None
    image_generated_bytes = None

    path_img = os.path.join(os.path.dirname(__file__), "..", "img")
    path_doc = os.path.join(os.path.dirname(__file__), "..", "doc")
    path_api_key = os.path.join(os.path.dirname(__file__), "..", "api.key")
    path_doc_config = os.path.join(path_doc, "doc_config.json")
    path_img_default = os.path.join(path_img, "image_default.png")

    try:
        with open(path_doc_config, 'r') as f:
            doc_config = json.load(f)
    except:
        doc_config = {}

    with open(path_api_key, "r") as api_key_open:
        api_key = api_key_open.read()
        
    def __init__(self):
        super().__init__()

        self.title(self.title_)
        self.geometry(f"{self.size_window[0]}x{self.size_window[1]}")
        self.wm_iconbitmap()
        icon_photo_path = self.path_img_default
        icon_photo = PhotoImage(file=icon_photo_path)
        self.iconphoto(False, icon_photo)

        # tabview
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.tabview = customtkinter.CTkTabview(self)
        self.tabview.grid(row=0, column=0, padx=self.padx_grid, pady=self.pady_grid, sticky="nsew")
        for tab in self.tab_names:
            self.tabview.add(tab)

        # tab-0
        tmp_tab = 0
        self.tabview.tab(self.tab_names[tmp_tab]).grid_rowconfigure(1, weight=1)
        self.tabview.tab(self.tab_names[tmp_tab]).grid_columnconfigure(0, weight=1)

        self.frame_role = customtkinter.CTkFrame(self.tabview.tab(self.tab_names[tmp_tab]), fg_color="transparent")
        self.frame_role.grid(row=0, column=0, padx=self.padx_grid, pady=(self.pady_grid, 0), sticky="nsew")
        self.frame_role.grid_columnconfigure(0, weight=1)

        self.frame_text = customtkinter.CTkFrame(self.tabview.tab(self.tab_names[tmp_tab]), fg_color="transparent")
        self.frame_text.grid(row=1, column=0, padx=self.padx_grid, pady=(self.pady_grid, 0), sticky="nsew")
        self.frame_text.grid_rowconfigure(0, weight=1)
        self.frame_text.grid_columnconfigure(0, weight=1)

        self.frame_message = customtkinter.CTkFrame(self.tabview.tab(self.tab_names[tmp_tab]), fg_color="transparent")
        self.frame_message.grid(row=2, column=0, padx=self.padx_grid, pady=self.pady_grid, sticky="nsew")
        self.frame_message.grid_columnconfigure(0, weight=1)

        self.entry_role = customtkinter.CTkEntry(self.frame_role, placeholder_text=self.placeholder_role, justify="center")
        self.entry_role.grid(row=0, column=0, sticky="nsew")

        self.textbox = customtkinter.CTkTextbox(self.frame_text, activate_scrollbars=False, state="disabled")
        self.textbox.grid(row=0, column=0, sticky="nsew")

        self.textbox_scrollbar = customtkinter.CTkScrollbar(self.frame_text, command=self.textbox.yview)
        self.textbox_scrollbar.grid(row=0, column=1, sticky="ns")

        self.textbox.configure(yscrollcommand=self.textbox_scrollbar.set)

        self.entry_message = customtkinter.CTkEntry(self.frame_message, placeholder_text=self.placeholder_message)
        self.entry_message.grid(row=0, column=0, sticky="nsew")

        self.button_send_message = customtkinter.CTkButton(self.frame_message, text="Send", width=55, border_width=self.border_width, border_color=self.border_color, command=self.send_message)
        self.button_send_message.grid(row=0, column=1, padx=(self.padx_grid, 0), sticky="e")

        # tab-1
        tmp_tab = 1
        self.tabview.tab(self.tab_names[tmp_tab]).grid_rowconfigure(1, weight=1)
        self.tabview.tab(self.tab_names[tmp_tab]).grid_columnconfigure(0, weight=1)

        self.frame_prompt = customtkinter.CTkFrame(self.tabview.tab(self.tab_names[tmp_tab]))
        self.frame_prompt.grid(row=0, column=0, padx=self.padx_grid, pady=(self.pady_grid, 0), sticky="nsew")
        self.frame_prompt.grid_columnconfigure(0, weight=1)

        self.frame_image = customtkinter.CTkFrame(self.tabview.tab(self.tab_names[tmp_tab]))
        self.frame_image.grid(row=1, column=0, padx=self.padx_grid, pady=(self.pady_grid, 0), sticky="nsew")
        self.frame_image.grid_rowconfigure(0, weight=1)
        self.frame_image.grid_columnconfigure(0, weight=1)

        self.frame_generate = customtkinter.CTkFrame(self.tabview.tab(self.tab_names[tmp_tab]))
        self.frame_generate.grid(row=2, column=0, padx=self.padx_grid, pady=self.pady_grid, sticky="nsew")
        self.frame_generate.grid_columnconfigure(0, weight=1)

        self.entry_prompt = customtkinter.CTkEntry(self.frame_prompt, placeholder_text=self.placeholder_generate, justify="center")
        self.entry_prompt.grid(row=0, column=0, sticky="nsew")

        image = customtkinter.CTkImage(dark_image=Image.open(self.path_img_default),
                                       size=self.size_image_logo)

        self.label_image = customtkinter.CTkLabel(self.frame_image, image=image, text="", justify="center")
        self.label_image.grid(row=0, column=0, padx=self.padx_grid, pady=self.pady_grid)

        self.button_generate_image = customtkinter.CTkButton(self.frame_generate, text="Generate", border_width=self.border_width, border_color=self.border_color, command=self.generate_image)
        self.button_generate_image.grid(row=0, column=0, sticky="nsew")

        # tab-2
        tmp_tab = 2
        self.tabview.tab(self.tab_names[tmp_tab]).grid_rowconfigure(0, weight=1)
        self.tabview.tab(self.tab_names[tmp_tab]).grid_columnconfigure(0, weight=1)

        self.frame_docs = customtkinter.CTkFrame(self.tabview.tab(self.tab_names[tmp_tab]), fg_color="transparent")
        self.frame_docs.grid(row=0, column=0, padx=self.padx_grid, pady=0, sticky="nsew")
        self.frame_docs.grid_rowconfigure(0, weight=1)
        self.frame_docs.grid_columnconfigure(0, weight=1)

        self.frame_add_doc = customtkinter.CTkFrame(self.tabview.tab(self.tab_names[tmp_tab]), fg_color="transparent")
        self.frame_add_doc.grid(row=1, column=0, padx=self.padx_grid, pady=self.pady_grid, sticky="nsew")
        self.frame_add_doc.grid_columnconfigure(0, weight=1)

        self.frame_docs_scrollable = customtkinter.CTkScrollableFrame(self.frame_docs)
        self.frame_docs_scrollable.grid(row=0, column=0, sticky="nsew")
        self.frame_docs_scrollable.grid_columnconfigure(1, weight=1)

        self.button_add_part = customtkinter.CTkButton(self.frame_add_doc, text="Add Doc", width=75, border_width=self.border_width, border_color=self.border_color, command=self.add_doc)
        self.button_add_part.grid(row=1, column=0, padx=(0, 2*self.padx_grid+6), pady=0, sticky="e")

        # bind
        self.bind('<Return>', self.click_return)
        self.bind('<Alt-Right>', self.click_arrow_right)
        self.bind('<Alt-Left>', self.click_arrow_left)
        self.bind("<Up>", self.click_up)
        self.bind("<Down>", self.click_down)
        self.bind("<Configure>", self.resize)

        # load docs
        self.load_docs()

    def send_message(self):
        message = self.entry_message.get()
        if not message:
            return
        self.button_send_message.configure(state="disabled")
        if self.first_message:
            role = self.entry_role.get()
            role_exp = f"{role} {self.role_suffix}"
            self.textbox.configure(state="normal")
            self.textbox.insert("end", f"Role: {role}\n")
            self.textbox.configure(state="disabled")
            self.chatgpt = ChatGPT(api_key=self.api_key, role=role_exp)
            self.first_message = False
        self.textbox.configure(state="normal")
        self.textbox.insert("end", f"> {message}\n")
        self.textbox.insert("end", f"> ...\n")
        self.textbox.see("end")
        self.textbox.configure(state="disabled")
        self.entry_message.delete(0, "end")
        thead = threading.Thread(target=self.send_message_thread,
                                 kwargs={"message": message})
        thead.start()

    def send_message_thread(self, message):
        answer = self.chatgpt.message(message=message)
        self.textbox.configure(state="normal")
        self.textbox.delete("end-5c", "end")
        self.textbox.insert("end", f"{answer}\n")
        self.textbox.configure(state="disabled")
        self.button_send_message.configure(state="normal")

    def generate_image(self):
        prompt = self.entry_prompt.get()
        if not prompt:
            return
        self.button_generate_image.configure(state="disabled")
        thread = threading.Thread(target=self.generate_image_thread,
                                  kwargs={"prompt": prompt})
        thread.start()

    def generate_image_thread(self, prompt):
        dall_e = DALLE(api_key=self.api_key)
        url = dall_e.generate(prompt=prompt)
        self.image_generated_content = requests.get(url).content
        self.image_generated_bytes = io.BytesIO(self.image_generated_content)
        image_generated = customtkinter.CTkImage(
            dark_image=Image.open(self.image_generated_bytes),
            size=self.size_image_logo)
        self.label_image.configure(image=image_generated)
        self.button_generate_image.configure(state="normal")

    def add_doc(self, doc={}):
        if doc:
            hash_ = doc["hash"]
            name_ = doc["name"]
            type_ = doc["type"]
            image_to_open = os.path.join(self.path_doc, name_, f"{name_}.png")
        else:
            hash_ = str(len(self.doc_config))
            while True:
                name_ = self.input_dialog(text="Enter the name of the doc:",
                                          title="Name of Doc")
                if not name_:
                    return
                path_doc = os.path.join(self.path_doc, name_)
                if not os.path.exists(path_doc):
                    break
            type_ = 0
            os.makedirs(path_doc)
            self.save_chat(name=name_)
            if self.image_generated_bytes:
                self.save_image(name=name_)
                image_to_open = self.image_generated_bytes
            else:
                image_to_open = os.path.join(self.path_doc, name_, f"{name_}.png")
                shutil.copyfile(self.path_img_default, image_to_open)
            data = {hash_: {"state": 1,
                            "hash": hash_,
                            "name": name_,
                            "type": type_}}
            self.doc_config.update(data)
            self.update_doc_config()
            doc = data[hash_]
        image_doc = customtkinter.CTkImage(dark_image=Image.open(image_to_open),
                                           size=self.size_image_docs)
        n = len(self.doc_widgets[0])
        self.doc_widgets[0].append(
            customtkinter.CTkLabel(self.frame_docs_scrollable, image=image_doc, text="", justify="center", cursor="hand2")
        )
        self.doc_widgets[1].append(
            customtkinter.CTkEntry(self.frame_docs_scrollable)
        )
        self.doc_widgets[2].append(
            customtkinter.CTkComboBox(self.frame_docs_scrollable, values=self.doc_types, width=100, justify="c", state="readonly", command=lambda type_=type_, n=n: self.update_type(n, type_))
        )
        self.doc_widgets[3].append(
            customtkinter.CTkButton(self.frame_docs_scrollable, text="Delete", width=75, border_width=self.border_width, border_color=self.border_color, command=lambda n=n: self.delete_doc(n))
        )
        self.doc_widgets[4].append(hash_)
        self.doc_widgets[0][n].grid(row=n, column=0, padx=(0, 0), pady=(self.pady_grid, 0), sticky="ew")
        self.doc_widgets[0][n].bind("<Button-1>", lambda event, name=doc["name"]: self.open_doc(name))
        self.doc_widgets[1][n].grid(row=n, column=1, padx=(self.padx_grid, 0), pady=(self.pady_grid, 0), sticky="ew")
        self.doc_widgets[1][n].configure(state="normal")
        self.doc_widgets[1][n].delete(0, "end")
        self.doc_widgets[1][n].insert(0, name_)
        self.doc_widgets[1][n].configure(state="disabled")
        self.doc_widgets[2][n].grid(row=n, column=2, padx=(self.padx_grid, 0), pady=(self.pady_grid, 0), sticky="ew")
        self.doc_widgets[2][n].set(self.doc_types[type_])
        self.doc_widgets[3][n].grid(row=n, column=3, padx=self.padx_grid, pady=(self.pady_grid, 0), sticky="ew")

    def delete_doc(self, n):
        hash = self.doc_widgets[4][n]
        self.doc_config[hash]["state"] = 0
        self.update_doc_config()
        if self.doc_widgets[0][n]:
            self.doc_widgets[0][n].destroy()
            self.doc_widgets[1][n].destroy()
            self.doc_widgets[2][n].destroy()
            self.doc_widgets[3][n].destroy()
            self.doc_widgets[0][n] = ""
            self.doc_widgets[1][n] = ""
            self.doc_widgets[2][n] = ""
            self.doc_widgets[3][n] = ""
            self.doc_widgets[4][n] = "" 

    def input_dialog(self, text, title):
        dialog = customtkinter.CTkInputDialog(text=text, title=title)
        return dialog.get_input()

    def save_chat(self, name):
        path_txt = os.path.join(self.path_doc, name, f"{name}.txt")
        with open(path_txt, 'w') as f:
            f.write(self.textbox.get(0.0, "end"))

    def save_image(self, name):
        path_png = os.path.join(self.path_doc, name, f"{name}.png")
        with open(path_png, "wb") as f:
            f.write(self.image_generated_content)

    def load_docs(self):
        for doc in self.doc_config.values():
            if doc["state"]:
                self.add_doc(doc)

    def update_doc_config(self):
        with open(self.path_doc_config, "w") as f:
            json.dump(self.doc_config, f, indent=4)

    def update_type(self, n, type_):
        hash = self.doc_widgets[-1][n]
        self.doc_config[hash]["type"] = self.doc_types.index(type_)
        self.update_doc_config()

    def open_doc(self, name):
        path_chat=os.path.join(self.path_doc, name, f"{name}.txt")
        path_logo=os.path.join(self.path_doc, name, f"{name}.png")
        AppOpenAIOpenDoc(name=name,
                         path_chat=path_chat,
                         path_logo=path_logo)

    def click_return(self, event):
        if self.tabview.get() == self.tab_names[0]:
            self.send_message()
        if self.tabview.get() == self.tab_names[1]:
            self.generate_image()

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

    def click_up(self, event):
        if self.tabview.get() == self.tab_names[0]:
            self.textbox.yview_scroll(-1, "units")

    def click_down(self, event):
        if self.tabview.get() == self.tab_names[0]:
            self.textbox.yview_scroll(1, "units")

    def resize(self, event) -> None:
        if self.winfo_width() < self.size_window[0]:
            self.geometry(f'{self.size_window[0]}x{self.winfo_height()}')
        if self.winfo_height() < self.size_window[1]:
            self.geometry(f'{self.winfo_width()}x{self.size_window[1]}')


if __name__ == "__main__":
    # AppOpenAI
    customtkinter.set_appearance_mode("dark")
    app_openai = AppOpenAI()
    app_openai.mainloop()
