from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend



def generate_key(key_path):
    key = rsa.generate_private_key(
        backend=crypto_default_backend(),
        public_exponent=65537,
        key_size=2048
    )
    private_key = key.private_bytes(
        crypto_serialization.Encoding.PEM,
        crypto_serialization.PrivateFormat.PKCS8,
        crypto_serialization.NoEncryption())
    public_key = key.public_key().public_bytes(
        crypto_serialization.Encoding.OpenSSH,
        crypto_serialization.PublicFormat.OpenSSH
    )

    print(private_key.decode("utf-8"))
    print(public_key.decode("utf-8"))

    print('write to:', key_path)

    with open(key_path, "w") as text_file:
        text_file.write(private_key.decode("utf-8"))


    with open(key_path + '.pub', "w") as text_file:
        public_file.write(public_key.decode("utf-8"))


    print('Finished write')
