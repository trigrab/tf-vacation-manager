from paramiko import SSHClient, AutoAddPolicy
from paramiko.ssh_exception import AuthenticationException
from scp import SCPClient


def connect_to_server(server, filename, user, key_filename=None, password=None):
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    #ssh.load_system_host_keys()
    try:
        ssh.connect(server, username=user, key_filename=key_filename, password=password)
    except AuthenticationException as e:
        print("Could not connect to server")
        print(e)
        return None
    return ssh

def upload_vacation_file(server, filename, user, key_filename=None, password=None):
    ssh = connect_to_server(server, filename, user, key_filename, password)

    if ssh is None:
        return False

    scp = SCPClient(ssh.get_transport())
    scp.put(filename)
    scp.close()
    return True

def delete_vacation_file(server, filename, user, key_filename=None, password=None):
    ssh = connect_to_server(server, filename, user, key_filename, password)

    if ssh is None:
        return False
    # ssh.set_missing_host_key_policy(AutoAddPolicy())
    ssh.load_system_host_keys()
    ssh.connect(server, username=user, key_filename=key_filename)
    ssh.exec_command('rm ' + filename)
    return True
