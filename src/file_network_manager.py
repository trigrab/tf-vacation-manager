from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient


def upload_vacation_file(server, filename, user, key_filename=None):
    ssh = SSHClient()
    # ssh.set_missing_host_key_policy(AutoAddPolicy())
    ssh.load_system_host_keys()
    ssh.connect(server, username=user, key_filename=key_filename)
    scp = SCPClient(ssh.get_transport())

    scp.put(filename)

    scp.close()

def delete_vacation_file(server, filename, user, key_filename=None):
    ssh = SSHClient()
    # ssh.set_missing_host_key_policy(AutoAddPolicy())
    ssh.load_system_host_keys()
    ssh.connect(server, username=user, key_filename=key_filename)
    ssh.exec_command('rm ' + filename)
