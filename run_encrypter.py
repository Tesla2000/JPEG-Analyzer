from classes.Jpeg_Image import JpegImage
from classes.rsa import RSA

# rsa = RSA()
# c = [0x12, 0x13, 0x14, 0x15]
# test = rsa.list_encrypt_cfb(c, 3)
# print(test)
# print(len(test[0]))
# test2 = rsa.list_decrypt_cfb(test[0], 3, test[1])
# print(test2)

jpeg = JpegImage('JPEG_JFIF.jpg', 16)
jpeg.read_markers()
jpeg.save_encrypted()
jpeg.save_decrypted()
