[![PyPI version](https://badge.fury.io/py/pysteg.svg)](https://badge.fury.io/py/pysteg)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pysteg)

# `pysteg`
`pysteg` is a python library for image steganography.

From Wikipedia:  
> Steganography is the practice of concealing a message within another message or a physical object.  
In computing/electronic contexts, a computer file, message, image, or video is concealed within another file, message, image, or video.  
The word steganography comes from Greek steganographia, which combines the words steganós (στεγανός), meaning "covered or concealed", and -graphia (γραφή) meaning "writing".

# Usage
```python
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
```

# Dependencies
`cryptography` and `imageio`  
Built with `poetry`

# License
MIT
