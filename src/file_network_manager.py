from paramiko import SSHClient, AutoAddPolicy
from paramiko.ssh_exception import AuthenticationException, SSHException
from scp import SCPClient
from tkinter import Frame, Label, ttk, StringVar, Tk, Toplevel, RIGHT, LEFT


class FileNetworkManager():

    def __init__(self, server, username, tk_root, key_filename=None, password=None):
        self.tk_root = tk_root
        self.root = None
        self.server = server
        self.username = username
        self.key_filename = key_filename
        self.password = password
        self.password_field = StringVar()
        self.main_frame = None


    def close_password_input_window(self):
        self.main_frame.destroy()
        self.root.destroy()
        print("Close window")
        self.password = self.password_field.get()
        self.connect_to_server()

    def close_and_upload_key(self):
        self.close_password_input_window()
        public_keyfile_name = self.key_filename + ".pub"
        with open(public_keyfile_name, 'r') as key:
            key = key.readline()
            # print('echo "' + key + '" >> .ssh/authorized_keys')
            self.ssh.exec_command('echo "' + key + '" >> .ssh/authorized_keys')

    def create(self):
        self.root = Toplevel(self.tk_root)
        self.main_frame = Frame(self.root, pady=15, padx=15)
        self.main_frame.pack(expand=True, fill="both")

        Label(self.main_frame, justify="left", text="Password").pack(anchor="w", pady=(15, 0))
        ttk.Entry(self.main_frame,
                  textvariable=self.password_field,
                  width=100, show='*').pack(anchor="w")

        ttk.Button(self.main_frame, text='Connect', command=self.close_password_input_window).pack(side=LEFT, pady=(15, 0))
        ttk.Button(self.main_frame, text='Connect and upload Key', command=self.close_and_upload_key).pack(side=RIGHT,
                                                                                                   pady=(15, 0))

        self.main_frame.wait_window(self.main_frame)

    def connect_to_server(self):
        self.ssh = SSHClient()
        self.ssh.set_missing_host_key_policy(AutoAddPolicy())
        #ssh.load_system_host_keys()
        try:
            self.ssh.connect(self.server, username=self.username, key_filename=self.key_filename, password=self.password)
        except AuthenticationException as e:
            print("Could not connect to server")
            # print(e)
            self.create()
        except SSHException as e:
            print("Could not connect to server")
            # print(e)
            self.create()
        except FileNotFoundError as e:
            print('No keyfile')
            # print(e)
            self.create()

    def upload_vacation_file(self, filename):
        self.connect_to_server()

        if self.ssh is None:
            return False

        scp = SCPClient(self.ssh.get_transport())
        scp.put(filename)
        scp.close()
        return True

    def delete_vacation_file(self, filename):
        self.connect_to_server()

        if self.ssh is None:
            return False
        # ssh.set_missing_host_key_policy(AutoAddPolicy())
        self.ssh.exec_command('rm ' + filename)
        return True

    def check_if_vacation_exists(self, filename):
        self.connect_to_server()
        _, stdout, error = self.ssh.exec_command('test -f "' + filename + '" && echo "True"')
        response = stdout.read()
        # print(response)
        if response != b'':
            return True
        else:
            return False
