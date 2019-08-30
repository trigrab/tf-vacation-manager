import os
from tkinter import Tk, Toplevel, Frame, Label, ttk, RIGHT, LEFT, Text, INSERT, END, StringVar
from tkinter.scrolledtext import ScrolledText


class TextEditor:
    def __init__(self, tk_root, template_file, template_text):
        self.tk_root = tk_root
        self.root = None
        self.main_frame = None
        self.editor_file = template_file
        self.editor_text = StringVar()
        self.editor_text.set(template_text)
        self.editor_text_field = None
        self._tkinter_vars = {}

    def create(self):
        self.root = Toplevel(self.tk_root)

        self.main_frame = Frame(self.root, pady=15, padx=15)
        self.main_frame.pack(expand=True, fill="both")

        self.editor_text_field = ScrolledText(self.main_frame)
        self.set_editor_text_field()
        self.editor_text_field.pack(anchor="w", pady=(15, 0))

        ttk.Button(self.main_frame, text='Save',
                   command=self.close_text_editor_with_save).pack(side=RIGHT,
                                                                  pady=(15, 0))
        ttk.Button(self.main_frame, text='Cancel',
                   command=self.close_text_editor_without_save).pack(side=LEFT, pady=(15, 0))

    def set_editor_text_field(self):
        self.editor_text_field.config(state='normal')
        self.editor_text_field["bg"] = "white"
        self.editor_text_field.tag_config("initial", background="white")
        self.editor_text_field.delete('1.0', END)
        self.editor_text_field.insert(INSERT, self.editor_text.get())

    def close_text_editor_without_save(self):
        self.main_frame.destroy()
        self.root.destroy()

    def close_text_editor_with_save(self):
        self.save_file()
        self.close_text_editor_without_save()

    def save_file(self):
        with open(os.path.join(self.editor_file), 'w') as editor_file_instance:
            editor_file_instance.writelines(self.editor_text_field.get("1.0", END))
