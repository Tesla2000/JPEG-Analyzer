import random
import sympy

class RSA:
    def __init__(self):
        self.p = 0
        self.q = 0
        while sympy.isprime(self.p) == False:
            self.p = random.randint(2**127, 2**128)
        while sympy.isprime(self.q) == False:
            self.q = random.randint(2**127, 2**128)
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)
        self.e = 5
        self.d = pow(self.e, -1, self.phi)


    def encrypt(self, m):
        self.c = pow(m, self.e, self.n)
        return self.c


    def decrypt(self, c):
        self.m = pow(c, self.d, self.n)
        return self.m


