from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend
import re
import os

def generate_key(key_path):
    # generate private/public key pair
    key = rsa.generate_private_key(backend=crypto_default_backend(), public_exponent=65537, \
        key_size=2048)

    # get public key in OpenSSH format
    public_key = key.public_key().public_bytes(crypto_serialization.Encoding.OpenSSH, \
        crypto_serialization.PublicFormat.OpenSSH)

    # get private key in PEM container format
    private_key = key.private_bytes(encoding=crypto_serialization.Encoding.PEM,
        format=crypto_serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=crypto_serialization.NoEncryption())

    key_path_parts = re.split(r"\\|/", key_path)
    print('path:', key_path_parts)
    key_path_parts = '\\'.join(key_path_parts[:-1])
    print('path:', key_path_parts)
    if not os.path.exists(key_path_parts):
        os.makedirs(key_path_parts)

    with open(key_path, "w") as text_file:
        text_file.write(private_key.decode("utf-8"))

    with open(key_path + '.pub', "w") as text_file:
        text_file.write(public_key.decode("utf-8"))
