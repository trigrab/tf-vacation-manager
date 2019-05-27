import logging
from datetime import datetime

from dateutil import tz
from jinja2 import FileSystemLoader, Environment
from tkinter import Tk, Frame, Label, StringVar, Text, INSERT, END
from pyDatePicker import Datepicker
import sys
import tkinter.ttk as ttk

from src.file_network_manager import FileNetworkManager

from src.Config import Config


logger = logging.getLogger("default")
logger.setLevel(logging.INFO)


class TFVacationManager:

    def __init__(self):
        self.config = Config()

        self.root = None

        self.template = self.get_template()

        self.set_window()

        self.file_network_manager = FileNetworkManager(server=self.config.server, username=self.config.username, tk_root=self.root,
                                                       key_filename=self.config.key_file)

        self.start_date = StringVar()
        self.start_date.set(self.get_localtime())
        self.end_date = StringVar()
        self.status = None
        self.vacation_text = StringVar()
        self.vacation_text.set(self.get_vacation_text())
        self.vacation_text_field = None

        self.build_window_structure()

        self.root.mainloop()

    @staticmethod
    def get_localtime():
        return datetime.now(tz.tzlocal()).date().strftime("%d.%m.%Y")

    @staticmethod
    def get_template():
        template_loader = FileSystemLoader(searchpath="./")
        template_env = Environment(loader=template_loader)
        template_file = "vacation_template.txt"
        return template_env.get_template(template_file)

    def get_vacation_text(self):
        return self.template.render(start_date=self.start_date.get(),
                                    end_date=self.end_date.get(),
                                    username=self.config.username)

    def write_vacation_file(self):
        self.vacation_text.set(self.get_vacation_text())
        self.set_vacation_text_field()

        logger.info("VacationFile stored in: %s \n Content:\n%s\n" % (self.config.file_path,
                                                                      self.vacation_text))

        self.status.config(text="text file written")
        path = self.config.file_path + '/' + self.config.file_name
        with open(path, "w") as file:
            file.write(self.vacation_text.get())

        self.file_network_manager.upload_vacation_file(filename=self.config.file_name)

    def set_window(self):
        self.root = Tk()
        self.root.geometry("600x600")
        self.root.title("VacationManager")

    def build_window_structure(self):
        main = Frame(self.root, pady=15, padx=15)
        main.pack(expand=True, fill="both")

        Label(main, justify="left", text="Urlaub vom").pack(anchor="w", pady=(15, 0))

        Datepicker(main, datevar=self.start_date).pack(anchor="w", )

        Label(main, justify="left", text="Urlaub bis").pack(anchor="w", pady=(15, 0))

        Datepicker(main, datevar=self.end_date).pack(anchor="w")

        ttk.Button(main, text="set", width=10, command=self.write_vacation_file).pack(anchor="w",
                                                                                      pady=(15, 0))

        ttk.Button(main, text="unset", width=10,
                   command=self.delete_vacation_file).pack(anchor="w", pady=(15, 0))

        self.status = Label(main, justify="left", textvariable=self.status)

        self.status.pack(anchor="w", pady=(15, 0))

        self.vacation_text_field = Text(main)
        self.set_vacation_text_field()
        self.vacation_text_field.pack(anchor="w", pady=(15, 0))

        if 'win' not in sys.platform:
            style = ttk.Style()
            style.theme_use('clam')

    def set_vacation_text_field(self):
        self.vacation_text_field.config(state='normal')
        self.vacation_text_field.delete('1.0', END)
        self.vacation_text_field.insert(INSERT, self.vacation_text.get())
        self.vacation_text_field.config(state='disabled')

    def delete_vacation_file(self):
        self.file_network_manager.delete_vacation_file(filename=self.config.file_name)


if __name__ == '__main__':
    TFVacationManager()
