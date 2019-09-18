from tkinter import Frame, Label, ttk, StringVar, Tk, Toplevel

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
    file_encoding = 'utf-8'

    def __init__(self):
        self.read()
        self.main = None
        self.root = None

    def create(self, tk_root=None):
        self._tkinter_vars['vars'] = {}

        self.root = Tk() if tk_root is None else Toplevel(tk_root)
        self.main = Frame(self.root, pady=15, padx=15)
        self.main.pack(expand=True, fill="both")

        for key in self.get_save_member_list():
            value = getattr(self, key)
            Label(self.main, justify="left", text=key).pack(anchor="w", pady=(15, 0))
            self._tkinter_vars['vars'][key] = StringVar()
            self._tkinter_vars['vars'][key].set(value)
            ttk.Entry(self.main,
                      textvariable=self._tkinter_vars['vars'][key],
                      width=100).pack(anchor="w")

        ttk.Button(self.main, text='Save', command=self.save).pack(anchor="w", pady=(15, 0))

        self.main.wait_window(self.main)

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

        self.main.destroy()
        self.root.destroy()

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