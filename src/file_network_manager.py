from paramiko import SSHClient, AutoAddPolicy
from paramiko.ssh_exception import AuthenticationException, SSHException
from scp import SCPClient
from tkinter import Frame, Label, ttk, StringVar, Tk


class FileNetworkManager():

    def __init__(self, server, username, key_filename=None, password=None):
        self.root = None
        self.server = server
        self.username = username
        self.key_filename = key_filename
        self.password = password


    def close_password_input_window(self):
        self.root.destroy()


    def create(self):
        self.root = Tk()
        self.root.geometry("300x450")
        self.root.title = "VacationManager"

        main = Frame(pady=15, padx=15)
        main.pack(expand=True, fill="both")

        Label(main, justify="left", text="Password").pack(anchor="w", pady=(15, 0))
        password_field = StringVar()
        ttk.Entry(main,
                  textvariable=password_field,
                  width=100).pack(anchor="w")

        ttk.Button(main, text='Connect', command=self.close_password_input_window()).pack(anchor="w", pady=(15, 0))

        main.wait_window(main)

        self.password = password_field.get()
        self.connect_to_server()


    def connect_to_server(self):
        self.ssh = SSHClient()
        self.ssh.set_missing_host_key_policy(AutoAddPolicy())
        #ssh.load_system_host_keys()
        try:
            self.ssh.connect(self.server, username=self.username, key_filename=self.key_filename, password=self.password)
        except AuthenticationException as e:
            print("Could not connect to server")
            print(e)
            self.create()
        except SSHException as e:
            print("Could not connect to server")
            print(e)
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
