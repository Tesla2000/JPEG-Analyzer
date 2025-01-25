import struct
import sys
from os import PathLike
from typing import Literal
from typing import Union

import cv2 as cv
import numpy as np

from chunk_info.chunk_dict import *
from classes.rsa import RSA
from protocols.protocols import File


class JpegImage:

    def __init__(self, filename: Union[PathLike[bytes], PathLike[str], bytes, int, str], enc_block_size: int=4):
        if enc_block_size >= 32:  # Decryption doesn't work if block size >= 32
            print("Warning! Block size too big! Setting block size value to 31")
            enc_block_size = 31
        self.enc_block_size = enc_block_size
        self.rsa = RSA()
        self.name = filename
        file = open(self.name, "rb")
        self.binary_img = list(file.read())
        file.close()
        self.markers = []
        self.anon = []
        self.app0 = []
        self.dht = []
        self.sos_data = []
        self.encrypted_img = []
        self.decrypted_img = []
        self.encrypted_dht = []
        self.encrypted_sos = []

    def get_segment_length(self, begin: int):
        return (self.binary_img[begin] << 8) | self.binary_img[begin + 1]

    def read_markers(self):
        i = 0
        while i < len(self.binary_img):
            if self.binary_img[i] == 0xff:
                next_byte = self.binary_img[i + 1]
                i += 2
                if next_byte != 0x00:
                    self.markers.append(marker_dict.get(next_byte, "UNKNOWN"))
                    if not (0xd0 <= next_byte <= 0xd9):  # no payload marker
                        if next_byte == 0xda:
                            i += self.get_segment_length(i)
                            end = self.read_sos(i)
                            self.sos_data.append([])
                            self.sos_data[-1] += self.binary_img[i:i + end]
                            i += end
                        else:
                            if next_byte == 0xe0:
                                self.app0 = self.binary_img[i:i + self.get_segment_length(i)]
                            if next_byte == 0xc4:
                                self.dht.append([])
                                self.dht[-1] = self.binary_img[i+2:i + self.get_segment_length(i)]
                            i += self.get_segment_length(i)
                    elif next_byte == 0xd9:
                        break
            else:
                i += 1

    def read_sos(self, begin: int):
        end = 0
        for i in range(begin, len(self.binary_img)):
            if self.binary_img[i] == 0xff:
                if self.binary_img[i + 1] != 0x00:
                    if not (0xd0 <= self.binary_img[i + 1] <= 0xd7):
                        end = i
                        break
        return end - begin

    def anonymize(self):
        i = 0
        while i < len(self.binary_img):
            if self.binary_img[i] == 0xff:
                next_byte = self.binary_img[i + 1]
                i += 2
                if next_byte in necessary_chunks:
                    self.anon += [0xff, next_byte]
                    if not (0xd0 <= next_byte <= 0xd9):  # no payload marker
                        self.anon += self.binary_img[i:i + self.get_segment_length(i)]
                        i += self.get_segment_length(i)
                        if next_byte == 0xda:
                            end = self.read_sos(i)
                            self.anon += self.binary_img[i:i + end]
                            i += end
                elif next_byte != 0x00:
                    i += self.get_segment_length(i)
            else:
                i += 1

    def save_anon(self):
        self.anonymize()
        file = open("anon.jpg", "wb")
        file.write(bytes(self.anon))
        file.close()

    def parse_app0(self):
        if not self.app0:
            print("No APP0 marker found!")
        else:
            app0_info = "APP0 Identifier: "
            for c in self.app0[2:6]:
                app0_info += chr(c)
            app0_info += "\nVer: " + str(self.app0[7]) + "." + f"{self.app0[8]:02}" + "\n"
            app0_info += "Density units: " + str(self.app0[9]) + "\n"
            app0_info += "XDensity: " + str((self.app0[10] << 8) | self.app0[11]) + "\n"
            app0_info += "YDensity: " + str((self.app0[12] << 8) | self.app0[13]) + "\n"
            app0_info += "XThumbnail: " + str(self.app0[14]) + "\n"
            app0_info += "YThumbnail: " + str(self.app0[15]) + "\n"
            print(app0_info)

    def display_image(self):
        image = cv.imread(self.name, cv.IMREAD_COLOR)
        if image is None:
            sys.exit("Could not read the image.")

        image = cv.resize(image, (600, 800))
        cv.imshow("Test image", image)
        cv.waitKey(0)

    def DFT_magnitude(self):
        image = cv.imread(self.name, cv.IMREAD_GRAYSCALE)
        if image is None:
            sys.exit("Could not read the image.")

        image = cv.resize(image, (600, 800))
        rows, cols = image.shape

        optimal_rows = cv.getOptimalDFTSize(rows)
        optimal_cols = cv.getOptimalDFTSize(cols)

        optimal_image = cv.copyMakeBorder(image, 0, optimal_rows - rows, 0,
                                          optimal_cols - cols, cv.BORDER_CONSTANT, value=[0, 0, 0])

        optimal_image = np.float32(optimal_image)

        # add new channel (plane) to our optimal_image
        complex_image = cv.merge([optimal_image, np.zeros(optimal_image.shape, np.float32)])

        cv.dft(complex_image, complex_image)

        planes = [np.zeros(optimal_image.shape, np.float32), np.zeros(optimal_image.shape, np.float32)]

        # DFT result is divided into Re and Im
        cv.split(complex_image, planes)

        amplitude_spectrum = np.zeros(optimal_image.shape, np.float32)

        # planes[0] = Re, planes[1] = Im
        cv.magnitude(planes[0], planes[1], amplitude_spectrum)

        # there shouldn't be zero in any cell before logarithm
        ones_matrix = np.ones(amplitude_spectrum.shape, np.float32)
        cv.add(ones_matrix, amplitude_spectrum, amplitude_spectrum)

        cv.log(amplitude_spectrum, amplitude_spectrum)

        # move quarters of the picture - coordinates of the input image(0,0) will be in the center of spectrum
        center_x = int(amplitude_spectrum.shape[0] / 2)
        center_y = int(amplitude_spectrum.shape[1] / 2)
        top_left = amplitude_spectrum[0:center_x, 0:center_y]
        top_right = amplitude_spectrum[center_x:center_x + center_x, 0:center_y]
        bottom_left = amplitude_spectrum[0:center_x, center_y:center_y + center_y]
        bottom_right = amplitude_spectrum[center_x: center_x + center_x, center_y: center_y + center_y]
        tmp = np.copy(top_left)
        amplitude_spectrum[0:center_x, 0:center_y] = bottom_right
        amplitude_spectrum[center_x: center_x + center_x, center_y: center_y + center_y] = tmp
        tmp = np.copy(top_right)
        amplitude_spectrum[center_x:center_x + center_x, 0:center_y] = bottom_left
        amplitude_spectrum[0:center_x, center_y: center_y + center_y] = tmp

        cv.normalize(amplitude_spectrum, amplitude_spectrum, 0, 1, cv.NORM_MINMAX)

        cv.imshow("Magnitude spectrum", amplitude_spectrum)
        cv.waitKey()

    def DFT_phase(self):
        image = cv.imread(self.name, cv.IMREAD_GRAYSCALE)
        if image is None:
            sys.exit("Could not read the image.")
        image = cv.resize(image, (600, 800))
        dft = np.fft.fft2(image)
        dft = np.fft.fftshift(dft)
        phase_spectrum = np.angle(dft)
        
        cv.imshow("Phase spectrum", phase_spectrum)
        cv.waitKey()

    def parse_exif(self):
        file = open(self.name, 'rb')
        content = file.read()
        try:
            offset = content.index(bytes.fromhex('FFE1'))
        except:
            print("Segment APP1 not found!")
            return
        file.seek(offset + 2)
        app1_data_size = file.read(2)
        print("APP1 data size:", int.from_bytes(app1_data_size, byteorder='big'))
        format = file.read(4)
        print("Format:", format.decode('utf-8'))
        file.seek(2, 1)
        start_tiff_header = file.tell()
        byte_align = file.read(2)
        if byte_align.decode('utf-8') == 'II':
            print("Little-endian")
            byte_align = 'little'
        else:
            print("Big-endian")
            byte_align = 'big'
        file.seek(2, 1)
        offset = file.read(4)
        offset = int.from_bytes(offset, byteorder=byte_align)
        file.seek(start_tiff_header + offset)

        print('METADATA FROM IFD0:')
        exif_offset, last_entry_adrress_ifd0 = self.read_entries(file, byte_align)

        print("METADATA FROM EXIF_SUBIFD:")
        file.seek(exif_offset + 12)
        self. read_entries(file, byte_align)

        print("METADATA FROM IFD1:")
        file.seek(last_entry_adrress_ifd0)
        offset = file.read(4)
        offset = int.from_bytes(offset, byteorder=byte_align)
        file.seek(offset + 12)
        self.read_entries(file, byte_align)
        file.close()

    def read_entries(self, file: File, byte_align: Literal['little', 'big']):
        number_entries = file.read(2)
        number_entries = int.from_bytes(number_entries, byte_align)
        start_first_entry = file.tell()
        for entry in range(1, number_entries + 1):
            file.seek(start_first_entry, 0)
            start_first_entry += 12
            tag = file.read(2)
            tag = int.from_bytes(tag, byteorder='little')
            if tag in TAGS:
                print(TAGS[tag], end=': ')
            else:
                continue
            data_format = file.read(2)
            data_format = int.from_bytes(data_format, byte_align)
            number_elements = file.read(4)
            number_elements = int.from_bytes(number_elements, byte_align)
            if (DATA_FORMAT[data_format][0] * number_elements) <= 4:
                data = file.read(4)
            else:
                offset = file.read(4)
                offset = int.from_bytes(offset, byte_align)
                file.seek(offset + 12)
                data = file.read(DATA_FORMAT[data_format][0] * number_elements)

            if DATA_FORMAT[data_format][1] == 'int':
                data = int.from_bytes(data, byteorder='little')
            elif DATA_FORMAT[data_format][1] == 'str':
                data = data.decode('ascii')
            elif DATA_FORMAT[data_format][1] == 'float':
                data = struct.unpack('f', data)
            elif DATA_FORMAT[data_format][1] == 'rational':
                data1 = int.from_bytes(data[0:4], byte_align)
                data2 = int.from_bytes(data[4:8], byte_align)
                data = str(data1) + '/' + str(data2)
            print(data)
            exif_offset = data
            last_entry_adrress = file.tell()
        print('----------------------------------------')
        return exif_offset, last_entry_adrress

    def encrypt_image(self):
        dht_encrypt = []
        sos_encrypt = []
        for dht in self.dht:
            dht_encrypt.append(self.rsa.list_encrypt(dht, self.enc_block_size))
        for sos in self.sos_data:
            sos_encrypt.append(self.rsa.list_encrypt_cfb(sos, self.enc_block_size))
            # sos_encrypt.append(self.rsa.list_encrypt(sos, self.enc_block_size))
        for dht in dht_encrypt:
            for idx, i in enumerate(dht[0]):
                if i == 0xff:
                    dht[0].insert(idx+1, 0x00)
        for sos in sos_encrypt:
            for idx, i in enumerate(sos[0]):
                if i == 0xff:
                    sos[0].insert(idx+1, 0x00)
        i = 0
        self.encrypted_dht = dht_encrypt
        self.encrypted_sos = sos_encrypt
        dht_index = 0
        sos_index = 0
        while i < len(self.binary_img):
            if self.binary_img[i] == 0xff:
                next_byte = self.binary_img[i + 1]
                i += 2
                self.encrypted_img += [0xff, next_byte]
                if not (0xd0 <= next_byte <= 0xd9):  # no payload marker
                    # if next_byte == 0xc4:  # Writing encrypted DHT (not working)
                    #     self.encrypted_img += list((len(dht_encrypt[dht_index][0])+2).to_bytes(2, byteorder='big'))
                    #     self.encrypted_img += dht_encrypt[dht_index][0]
                    #     dht_index += 1
                    #     i += self.get_segment_length(i)
                    # else:
                    self.encrypted_img += self.binary_img[i:i + self.get_segment_length(i)]
                    i += self.get_segment_length(i)
                    if next_byte == 0xda:  # Writing encrypted sos
                        end = self.read_sos(i)
                        self.encrypted_img += sos_encrypt[sos_index][0]
                        sos_index += 1
                        i += end
            else:
                i += 1

    def save_encrypted(self):
        self.encrypt_image()
        file = open("enc.jpg", "wb")
        file.write(bytes(self.encrypted_img))
        file.close()

    def decrypt_image(self):
        sos_decrypt = []
        for sos in self.encrypted_sos:
            for idx, i in enumerate(sos[0]):
                if i == 0xff:
                    sos[0].pop(idx+1)
        for sos in self.encrypted_sos:
            # sos_decrypt.append(self.rsa.list_decrypt(sos[0], self.enc_block_size, sos[1]))
            sos_decrypt.append(self.rsa.list_decrypt_cfb(sos[0], self.enc_block_size, sos[1]))
        i = 0
        sos_index = 0
        while i < len(self.binary_img):
            if self.binary_img[i] == 0xff:
                next_byte = self.binary_img[i + 1]
                i += 2
                self.decrypted_img += [0xff, next_byte]
                if not (0xd0 <= next_byte <= 0xd9):  # no payload marker
                    self.decrypted_img += self.binary_img[i:i + self.get_segment_length(i)]
                    i += self.get_segment_length(i)
                    if next_byte == 0xda:  # Writing decrypted sos
                        end = self.read_sos(i)
                        self.decrypted_img += sos_decrypt[sos_index]
                        sos_index += 1
                        i += end
            else:
                i += 1

    def save_decrypted(self):
        self.decrypt_image()
        file = open("dec.jpg", "wb")
        file.write(bytes(self.decrypted_img))
        file.close()
