import json
import logging
import subprocess
from subprocess import PIPE
from distutils.version import StrictVersion
import urllib.request
from datetime import datetime

from dateutil import tz
from jinja2 import FileSystemLoader, Environment, BaseLoader
from jinja2.exceptions import TemplateSyntaxError
from tkinter import Tk, Frame, Label, StringVar, Text, INSERT, END, messagebox, Menu, X

from tf_vacation_manager.src.TextEditor import TextEditor
from tf_vacation_manager.src.pyDatePicker import Datepicker
import sys
import tkinter.ttk as ttk

from tf_vacation_manager.src.file_network_manager import FileNetworkManager

from tf_vacation_manager.src.Config import Config
import os.path


logger = logging.getLogger("default")
logger.setLevel(logging.INFO)


class TFVacationManager:

    def __init__(self):
        self.config = Config()

        self.root = None
        self.set_window()

        self.template_file = "vacation_message.txt"
        self.template = self.get_template()

        self.file_network_manager = FileNetworkManager(server=self.config.server,
                                                       username=self.config.username,
                                                       tk_root=self.root,
                                                       key_filename=self.config.key_file)
        self.text_editor = None

        self.start_date = StringVar()
        self.start_date.set(self.get_localtime())
        self.start_date.trace('w', self.set_vacation_text_field)
        self.end_date = StringVar()
        self.end_date.trace('w', self.set_vacation_text_field)

        self.status = None
        self.vacation_text = StringVar()
        self.vacation_text_field = None

        self.build_window_structure()

        self.root.mainloop()

    @staticmethod
    def get_localtime():
        return datetime.now(tz.tzlocal()).date().strftime("%d.%m.%Y")

    def get_template(self):
        if not os.path.exists(os.path.join(self.config.working_directory, self.template_file)):
            script_path = os.path.dirname(os.path.realpath(__file__))
            with open(os.path.join(script_path, 'vacation_template.txt'),
                      'r', encoding=self.config.file_encoding) as default_template:
                with open(os.path.join(self.config.working_directory, self.template_file),
                          'w', encoding=self.config.file_encoding) as new_template_file:
                    new_template_file.writelines(default_template.readlines())

        try:
            template_loader = FileSystemLoader(searchpath=self.config.working_directory)
            template_env = Environment(loader=template_loader)
            template = template_env.get_template(self.template_file)

        except TemplateSyntaxError as e:
            messagebox.showerror(title="Syntax error", message="There is an error in your message:\n" + e.message +
                                                               "\nUsing default text.")
            script_path = os.path.dirname(os.path.realpath(__file__))
            template_loader = FileSystemLoader(searchpath=script_path)
            template_env = Environment(loader=template_loader)
            template = template_env.get_template('vacation_template.txt')
        return template


    def get_vacation_text(self):
        return self.template.render(start_date=self.start_date.get(),
                                    end_date=self.end_date.get(),
                                    username=self.config.username)

    def write_vacation_file(self):
        self.vacation_text.set(self.get_vacation_text())
        self.set_vacation_text_field()

        logger.info('VacationFile stored in: %s \n Content:\n%s\n' % (self.config.file_path,
                                                                      self.vacation_text))

        self.status.config(text='text file written')
        with open(self.config.file_name_path, 'w', encoding=self.config.file_encoding) as file:
            file.write(self.vacation_text.get())

        print(self.config.file_name_path)

        uploaded = self.file_network_manager.upload_vacation_file(filename=self.config.file_name_path)

        if uploaded and self.file_network_manager.check_if_vacation_exists(self.config.file_name):
            msg = 'Erfolgreich erstellt'
            messagebox.showinfo('Info', msg)
        else:
            msg = 'Uups etwas lief schief :('
            messagebox.showerror('Info', msg)

    def set_window(self):
        self.root = Tk()
        self.root.geometry('600x600')
        self.root.title('VacationManager')

    def build_window_structure(self):
        main = Frame(self.root, pady=15, padx=15)
        main.pack(expand=True, fill='both')
        menu = Menu(self.root)
        self.root.config(menu=menu)
        filemenu = Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Eigenschaften",
                             command=self.open_config)
        filemenu.add_command(label="Suche Updates",
                             command=self.check_for_update)
        filemenu.add_command(label="Update installieren",
                             command=self.update_module)
        Label(main, justify="left", text="Urlaub vom").pack(anchor="w", pady=(15, 0))

        Datepicker(main, datevar=self.start_date).pack(anchor="w", )

        Label(main, justify="left", text="Urlaub bis").pack(anchor="w", pady=(15, 0))

        Datepicker(main, datevar=self.end_date).pack(anchor="w")

        ttk.Button(main, text="Jetzt aktivieren", width=15, command=self.write_vacation_file).pack(anchor="w",
                                                                                      pady=(15, 0))

        ttk.Button(main, text="Jetzt deaktivieren", width=15,
                   command=self.delete_vacation_file).pack(anchor="w", pady=(15, 0))
        self.status = Label(main, justify="left", textvariable=self.status)

        self.status.pack(anchor="w", pady=(15, 0))
        ttk.Button(main, text='Editieren',
                   command=self.open_text_editor).pack(anchor="e",
                                                       pady=(0, 0))

        self.vacation_text_field = Text(main)
        self.vacation_text_field.pack(anchor="s", fill=X, pady=(15, 0))
        self.set_vacation_text_field()

        if 'win' not in sys.platform:
            style = ttk.Style()
            style.theme_use('clam')

    def set_vacation_text_field(self, *args):
        self.template = self.get_template()
        self.vacation_text.set(self.get_vacation_text())
        self.vacation_text_field.config(state='normal')
        self.vacation_text_field.delete('1.0', END)
        self.vacation_text_field.insert(INSERT, self.vacation_text.get())
        self.vacation_text_field.config(state='disabled')

    def delete_vacation_file(self):
        if self.file_network_manager.delete_vacation_file(filename=self.config.file_name):
            msg = "Erfolgreich deaktiviert"
            messagebox.showinfo("Info", msg)
        else:
            msg = 'Uups etwas lief schief :('
            messagebox.showerror("Info", msg)

    def open_config(self):
        self.config.create(tk_root=self.root)

    def open_text_editor(self):
        text_editor = self.text_editor = TextEditor(tk_root=self.root,
                                                    template_file=os.path.join(self.config.working_directory,
                                                                               self.template_file),
                                                    config=self.config)
        self.text_editor.create()
        self.root.wait_window(text_editor.root)

        self.set_vacation_text_field()

    @staticmethod
    def check_for_update():
        latest_release = TFVacationManager.get_latest_release_tag()
        latest_release = latest_release[1:]  # remove leading 'v' character from tag_name
        return StrictVersion(Config.module_version) <= StrictVersion(latest_release)

    @staticmethod
    def get_latest_release_tag():
        with urllib.request.urlopen(Config.github_api_repo + 'releases') as response:
            releases = json.load(response)
            return releases[0]['tag_name']

    def update_module(self):
        if self.check_for_update():
            subprocess.Popen('pip install ' + self.config.github_repo + '@'
                             + self.get_latest_release_tag(),
                             shell=True, stdin=PIPE, stdout=PIPE)
            exit()


if __name__ == '__main__':
    TFVacationManager()
