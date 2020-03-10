from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend



def generate_key(key_path):
    # generate private/public key pair
    key = rsa.generate_private_key(backend=default_backend(), public_exponent=65537, \
        key_size=2048)

    # get public key in OpenSSH format
    public_key = key.public_key().public_bytes(serialization.Encoding.OpenSSH, \
        serialization.PublicFormat.OpenSSH)

    # get private key in PEM container format
    private_key = key.private_bytes(encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption())

    print(private_key.decode("utf-8"))
    print(public_key.decode("utf-8"))

    print('write to:', key_path)

    with open(key_path, "w") as text_file:
        text_file.write(private_key.decode("utf-8"))


    with open(key_path + '.pub', "w") as text_file:
        text_file.write(public_key.decode("utf-8"))


    print('Finished write')
