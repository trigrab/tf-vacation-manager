import logging
from datetime import datetime

from dateutil import tz
from jinja2 import FileSystemLoader, Environment
from tkinter import Tk, Frame, Label, StringVar
from pyDatePicker import Datepicker
import sys
import tkinter.ttk as ttk

from src.file_network_manager import upload_vacation_file

logger = logging.getLogger("default")
logger.setLevel(logging.INFO)

username = "ntw"
file_path = "./"
file_name = ".vacation.txt"


class TFVacationManager:

    def __init__(self):
        self.root = None

        self.template = self.get_template()

        self.set_window()

        self.username = StringVar()
        self.username.set(username)
        self.start_date = StringVar()
        self.start_date.set(self.get_localtime())
        self.end_date = StringVar()
        self.status = None

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

    def write_vacation_file(self):
        vacation_file_content = self.template.render(start_date=self.start_date.get(),
                                                     end_date=self.end_date.get(),
                                                     username=self.username.get())
        logger.info("VacationFile stored in: %s \n Content:\n%s\n" % (file_path,
                                                                      vacation_file_content))

        self.status.config(text="text file written")
        path = file_path + '/' + file_name
        with open(path, "w") as file:
            file.write(vacation_file_content)

        upload_vacation_file(file_name, self.username.get())

    def set_window(self):
        self.root = Tk()
        self.root.geometry("500x600")
        self.root.title = "VacationManager"

    def build_window_structure(self):
        main = Frame(self.root, pady=15, padx=15)
        main.pack(expand=True, fill="both")

        Label(main, justify="left", text="username").pack(anchor="w", pady=(15, 0))
        ttk.Entry(main, textvariable=self.username).pack(anchor="w")

        Label(main, justify="left", text="Urlaub vom").pack(anchor="w", pady=(15, 0))

        Datepicker(main, datevar=self.start_date).pack(anchor="w", )

        Label(main, justify="left", text="Urlaub bis").pack(anchor="w", pady=(15, 0))

        Datepicker(main, datevar=self.end_date).pack(anchor="w")

        ttk.Button(main, text="set", width=10, command=self.write_vacation_file).pack(anchor="w",
                                                                                      pady=(15, 0))

        self.status = Label(main, justify="left", textvariable=self.status)

        self.status.pack(anchor="w", pady=(15, 0))
        if 'win' not in sys.platform:
            style = ttk.Style()
            style.theme_use('clam')


if __name__ == '__main__':
    TFVacationManager()
