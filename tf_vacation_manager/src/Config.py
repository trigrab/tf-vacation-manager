from tkinter import Frame, Label, ttk, StringVar, Tk, Toplevel

from yaml import load, dump
import os.path

static_parameters = ['module_version', 'file_encoding'
                     'github_url', 'github_api', 'github_api_repo', 'github_repo']


class Config:
    config_file = './config.yml'
    server = 'login.somewhere.some_uni.de'
    username = 'someone'
    file_path = './'
    file_name = '.vacation.txt'
    version = 1.0
    key_file = '.ssh/id_rsa'
    _tkinter_vars = {}
    file_encoding = 'utf-8'
    module_version = '0.1.4'
    github_api = "https://api.github.com/"
    github_url = "https://github.com/"
    github_api_repo = github_api + "repos/trigrab/tf-vacation-manager/"
    github_repo = github_url + "trigrab/tf-vacation-manager/"

    def __init__(self):
        self.config_file = self.find_config_file()
        working_directory = os.path.dirname(self.config_file)
        os.chdir(working_directory)
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
            if key in static_parameters:
                continue
            if hasattr(self, key):
                if not key.startswith('_') and not callable(getattr(self, key)) and \
                        key is not None and getattr(self, key) is not None:
                    if key == 'vars' or key == 'config_file':
                        continue
                    if not for_saving and key == 'version':
                        continue
                    member_list.append(key)
        return member_list

    def save(self):
        for key in self.get_save_member_list():
            value = self._tkinter_vars['vars'][key].get()
            # if isinstance(value, str):
                # if value[:2] == './':
                #     value = os.getcwd() + value
            if hasattr(self, key):
                setattr(self, key, value)

        if self.key_file is None or self.key_file == '':
            self.key_file = os.path.expanduser('~/.ssh/id_rsa')

        print('write config to:', self.config_file)

        with open(self.config_file, 'w', encoding=self.file_encoding) as config_file:
            yml_dict = {}
            for key in self.get_save_member_list(for_saving=True):
                yml_dict[key] = getattr(self, key)
                if yml_dict[key] == '':
                    yml_dict[key] = None
            dump(yml_dict, config_file)

        self.main.destroy()
        self.root.destroy()


    def find_config_file(self):
        if os.path.exists(self.config_file):
            return self.config_file

        app_data = os.getenv('APPDATA')
        home_dir = os.path.expanduser('~')
        if app_data is not None and os.path.exists(app_data):
            app_data += '/.tf-vacation-manager/config.yml'
            if os.path.exists(app_data):
                return app_data
            elif home_dir is None or not os.path.exists(home_dir + '/.tf-vacation-manager'):
                os.mkdir(os.path.dirname(app_data))
                return app_data


        else:
            if home_dir is not None:
                if not os.path.exists(home_dir + '/.tf-vacation-manager'):
                    os.mkdir(home_dir + '/.tf-vacation-manager')
                return home_dir + '/.tf-vacation-manager/config.yml'

        return self.config_file

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
