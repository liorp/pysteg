from base64 import urlsafe_b64encode
from hashlib import md5
from typing import Tuple, Iterator

import imageio
from cryptography.fernet import Fernet

from utils import str2bin


class Encryptor:
    """Responsible for steganography of many images and messages using a given key"""
    def __init__(self, password: str):
        _hash = md5(password.encode()).hexdigest()
        cipher_key = urlsafe_b64encode(_hash.encode())
        self.__encryptor = Fernet(cipher_key)

    def __get_data(self, message: str) -> Tuple[Iterator, str]:
        # Preparing the data for writing: length+data
        encrypted_message = self.__encryptor.encrypt(message.encode())
        data_length = format(len(encrypted_message)*8, '032b')
        data = iter(data_length + str2bin(encrypted_message.decode()))
        return data, data_length

    @staticmethod
    def __check_encoding_capacity(height: int, width: int, data_length: int) -> int:
        encoding_capacity = height * width * 3
        if data_length > encoding_capacity:
            raise ValueError("The data size is too big to fit in this image!")
        return encoding_capacity

    @staticmethod
    def __insert_data_to_image(im, data: str):
        new_im = im.copy()
        height, width, _ = new_im.shape
        modified_bits = 0
        try:
            for i in range(height):
                for j in range(width):
                    pixel = new_im[i, j]
                    for k in range(3):
                        # To replace the LSB with b, where b can be either 0 or 1, you can use (n & ~1) | b.
                        pixel[k] = (pixel[k] & ~1) | int(next(data))
                        modified_bits += 1
        except StopIteration:
            pass
        return new_im, modified_bits

    def encrypt(self, im, message: str, out_path: str = None) -> Tuple[bytes, float]:
        """
        Encrypts `message` inside `image` and writes output to `out_path`.
        Returns the encrypted image, and loss (percentage of how many bits were changed).
        """
        data, data_length = self.__get_data(message)
        height, width, _ = im.shape
        encoding_capacity = self.__check_encoding_capacity(height, width, int(data_length, 2))

        new_im, modified_bits = self.__insert_data_to_image(im, data)

        imageio.imwrite(out_path, new_im)
        loss_percentage = (modified_bits / encoding_capacity) * 100
        return im, loss_percentage

