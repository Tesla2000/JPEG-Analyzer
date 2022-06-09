from classes.rsa import RSA

rsa = RSA()

test = rsa.encrypt(20)
print(test)

test2 = rsa.decrypt(test)
print(test2)