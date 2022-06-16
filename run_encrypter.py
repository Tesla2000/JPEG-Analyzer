from classes.Jpeg_Image import JpegImage
# rsa = RSA()
# c = [0x12, 0x13, 0x14, 0x15]
# test = rsa.list_encrypt(c, 4)
# print(test)
# test2 = rsa.list_decrypt(test[0], 4, test[1])
# print(test2)

jpeg = JpegImage('JPEG_JFIF.jpg', 32)
jpeg.read_markers()
jpeg.save_encrypted()