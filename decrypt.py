from base64 import urlsafe_b64encode
from hashlib import md5

from cryptography.fernet import Fernet

from utils import bin2str


class Decryptor:
    """Responsible for decrypting steganography of many images using a given key"""
    def __init__(self, password: str):
        _hash = md5(password.encode()).hexdigest()
        cipher_key = urlsafe_b64encode(_hash.encode())
        self.__encryptor = Fernet(cipher_key)

    @staticmethod
    def __extract_data_from_image(im, data_length, header_length=32) -> str:
        data = ""
        height, width, _ = im.shape
        try:
            for i in range(height):
                for j in range(width):
                    pixel = im[i, j]
                    for k in range(3):
                        # Skip the header
                        if header_length:
                            header_length -= 1
                            continue

                        # Get the lsb
                        data += str(pixel[k] & 1)
                        data_length -= 1
                        if data_length == 0:
                            raise StopIteration
        except StopIteration:
            pass
        return bin2str(data)

    @staticmethod
    def __extract_data_length_from_image(im, header_length=32) -> int:
        data_length = ""
        height, width, _ = im.shape
        try:
            for i in range(height):
                for j in range(width):
                    pixel = im[i, j]
                    for k in range(3):
                        # Get the lsb
                        data_length += str(pixel[k] & 1)
                        header_length -= 1
                        if header_length == 0:
                            raise StopIteration
        except StopIteration:
            pass
        return int(data_length, 2)

    def decrypt(self, im) -> str:
        """Decrypts the hidden message in `im`."""
        data_length = self.__extract_data_length_from_image(im)
        data = self.__extract_data_from_image(im, data_length)
        message = self.__encryptor.decrypt(data.encode()).decode()
        return message

