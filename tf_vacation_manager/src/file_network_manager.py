from paramiko import SSHClient, AutoAddPolicy
from paramiko.ssh_exception import AuthenticationException, SSHException, NoValidConnectionsError
from scp import SCPClient
from tkinter import Frame, Label, ttk, StringVar, Tk, Toplevel, RIGHT, LEFT


class FileNetworkManager:

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
        self.password = self.password_field.get()
        self.key_filename = None
        self.connect_to_server()

    def close_and_upload_key(self):
        public_keyfile_name = self.key_filename
        self.close_password_input_window()
        self.key_filename = public_keyfile_name
        public_keyfile_name += ".pub"
        with open(public_keyfile_name, 'r') as key:
            key = key.readline()
            # print('echo "' + key + '" >> .ssh/authorized_keys')
            if self.ssh is None:
                return
            self.ssh.exec_command('echo "' + key + '" >> .ssh/authorized_keys')

    def window_closed(self):
        self.main_frame.destroy()
        self.root.destroy()
        self.ssh = None

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
        self.root.protocol("WM_DELETE_WINDOW", self.window_closed)
        self.main_frame.wait_window(self.main_frame)

    def connect_to_server(self):
        self.ssh = SSHClient()
        self.ssh.set_missing_host_key_policy(AutoAddPolicy())
        print("Load key file:", self.key_filename)
        # ssh.load_system_host_keys()
        try:
            self.ssh.connect(self.server, username=self.username, key_filename=self.key_filename,
                             password=self.password, look_for_keys=False)
        except AuthenticationException as e:
            print("Could not connect to server")
            # print(e)
            self.create()
        except SSHException as e:
            print("Could not connect to server")
            # print(e)
            self.create()
        except FileNotFoundError as e:
            print('No keyfile2')
            print(e)
            self.create()
        except NoValidConnectionsError as e:
            print("No valid connection")
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
        if self.ssh is None:
            return False
        _, stdout, error = self.ssh.exec_command('test -f "' + filename + '" && echo "True"')
        response = stdout.read()
        # print(response)
        if response != b'':
            return True
        else:
            return False
