import random
import sympy
from functions.rsa_misc import *


class RSA:
    def __init__(self):
        self.p = 0
        self.q = 0
        self.e = 0
        while not sympy.isprime(self.p):
            self.p = random.randint(2 ** 127, 2 ** 128)
        while not sympy.isprime(self.q):
            self.q = random.randint(2 ** 127, 2 ** 128)
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)
        while not euclidean(self.e, self.phi) == 1:
            self.e = random.randint(1, self.phi)  # public key
        self.d = pow(self.e, -1, self.phi)  # private key

    def encrypt(self, m):
        return pow(m, self.e, self.n)

    def decrypt(self, c):
        return pow(c, self.d, self.n)

    def list_encrypt(self, li, block_size):
        list_split, last_length = split(li, block_size)
        list_encrypted = []
        for i in list_split:
            list_encrypted += self.encrypt(int.from_bytes(i, byteorder='big')).to_bytes(32, byteorder='big')
        return list_encrypted, last_length

    def list_decrypt(self, li, block_size, last_len):
        list_split, last_length = split(li, 32)
        list_decrypted = []
        for i in list_split[:-1]:
            list_decrypted += self.decrypt(int.from_bytes(i, byteorder='big')).to_bytes(block_size, byteorder='big')
        list_decrypted += \
            self.decrypt(int.from_bytes(list_split[-1], byteorder='big')).to_bytes(last_len, byteorder='big')
        return list_decrypted

    def list_encrypt_cbc(self, li, block_size, init_vec=0):
        list_split, last_length = split(li, block_size)
        list_encrypted = [
            self.encrypt(int.from_bytes(list_split[0], byteorder='big') ^ init_vec).to_bytes(32, byteorder='big')]
        for i in range(1, len(list_split)):
            list_encrypted.append(self.encrypt(int.from_bytes(list_split[i], byteorder='big') ^ int.from_bytes(
                list_encrypted[i-1], byteorder='big')).to_bytes(32, byteorder='big'))
        list_encrypted = b''.join(list_encrypted)
        return list_encrypted, last_length

    def list_decrypt_cbc(self, li, block_size, last_len, init_vec=0):
        list_split, last_length = split(li, 32)
        list_decrypted = [
            (self.decrypt(int.from_bytes(list_split[0], byteorder='big')) ^
             init_vec).to_bytes(block_size, byteorder='big')]
        for i in range(1, len(list_split) - 1):
            list_decrypted.append((self.decrypt(int.from_bytes(
                list_split[i], byteorder='big') ^ int.from_bytes(list_split[i-1], byteorder='big'))).to_bytes(block_size, byteorder='big'))
        list_decrypted.append((self.decrypt(int.from_bytes(
            list_split[-1], byteorder='big') ^ int.from_bytes(list_split[-2], byteorder='big'))).to_bytes(last_len, byteorder='big'))
        list_decrypted = b''.join(list_decrypted)
        return list_decrypted

    def print_keys(self):
        print("Public key: ", self.e)
        print("Private key: ", self.d)
        print("N:", self.n)
