import imageio
from cryptography.fernet import Fernet

from encrypt import Encryptor
from decrypt import Decryptor


def load_image(path: str):
    return imageio.imread(path)


def load_password(password: str) -> Fernet:
    return Fernet(password.encode())


def main():
    in_path = "./dogcyber.png"
    out_path = "./dogscybersteg.png"
    password = "12345678"
    message = "My secret message!"

    im = load_image(in_path)

    encryptor = Encryptor(password)
    encryptor.encrypt(im, message, out_path)

    decryptor = Decryptor(password)
    print(decryptor.decrypt(load_image(out_path)))


if __name__ == '__main__':
    main()
