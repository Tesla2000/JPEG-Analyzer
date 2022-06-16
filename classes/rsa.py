import random
import sympy
from functions.rsa_misc import *


class RSA:
    def __init__(self):
        self.p = 0
        self.q = 0
        self.c = 0
        self.m = 0
        self.e = 0
        while not sympy.isprime(self.p):
            self.p = random.randint(2 ** 127, 2 ** 128)
        while not sympy.isprime(self.q):
            self.q = random.randint(2 ** 127, 2 ** 128)
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)
        while not euclidean(self.e, self.phi) == 1:
            self.e = random.randint(1, self.phi)
        self.d = pow(self.e, -1, self.phi)

    def encrypt(self, m):
        self.c = pow(m, self.e, self.n)
        return self.c

    def decrypt(self, c):
        self.m = pow(c, self.d, self.n)
        return self.m

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
