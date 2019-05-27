from tkinter import Frame, Label, ttk, StringVar, Tk

from yaml import load, dump
import os.path


class Config:
    config_file = './config.yml'
    server = 'login.somewhere.some_uni.de'
    username = 'someone'
    file_path = './'
    file_name = '.vacation.txt'
    version = 1.0
    key_file = '/home/someone/.ssh/id_rsa'
    _tkinter_vars = {}

    def __init__(self):
        self.read()

    def create(self):
        self._tkinter_vars['vars'] = {}

        root = Tk()
        root.geometry("300x450")
        root.title = "VacationManager"

        main = Frame(pady=15, padx=15)
        main.pack(expand=True, fill="both")

        for key in self.get_save_member_list():
            value = getattr(self, key)
            Label(main, justify="left", text=key).pack(anchor="w", pady=(15, 0))
            self._tkinter_vars['vars'][key] = StringVar()
            self._tkinter_vars['vars'][key].set(value)
            ttk.Entry(main,
                      textvariable=self._tkinter_vars['vars'][key],
                      width=100).pack(anchor="w")

        ttk.Button(main, text='Save', command=self.save).pack(anchor="w", pady=(15, 0))

        main.wait_window(main)

    def get_save_member_list(self, for_saving=False):
        member_list = []
        for key in dir(Config):
            if hasattr(self, key):
                if not key.startswith('_') and not callable(getattr(self, key)) and \
                        key is not None and getattr(self, key) is not None:
                    if key == 'vars' or key == 'config_file':
                        continue
                    if not for_saving and key == 'version' :
                        continue
                    member_list.append(key)
        return member_list

    def save(self):
        for key in self.get_save_member_list():
            value = self._tkinter_vars['vars'][key].get()
            if hasattr(self, key):
                setattr(self, key, value)

        with open(self.config_file, 'w') as config_file:
            yml_dict = {}
            for key in self.get_save_member_list(for_saving=True):
                yml_dict[key] = getattr(self, key)
                if yml_dict[key] == '':
                    yml_dict[key] = None
            dump(yml_dict, config_file)

    def read(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r+') as config_file:
                config_yml = load(config_file)

                for key, value in config_yml.items():
                    if key == 'version':
                        continue
                    if hasattr(self, key):
                        setattr(self, key, value)

                if config_yml['version'] != self.version:
                    self.create()
        else:
            self.create()
