import cv2 as cv
import sys
import numpy as np
from chunk_info.chunk_dict import TAGS, DATA_FORMAT
import struct


def display_image():
    image = cv.imread("test.jpg", cv.IMREAD_COLOR)
    if image is None:
        sys.exit("Could not read the image.")

    image = cv.resize(image, (600, 800)) 
    cv.imshow("Test image", image)
    cv.waitKey(0)




def DFT():
    image = cv.imread("test.jpg", cv.IMREAD_GRAYSCALE)
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

    cv.normalize (amplitude_spectrum, amplitude_spectrum, 0, 1, cv.NORM_MINMAX)

    cv.imshow("spectrum magnitude", amplitude_spectrum)
    cv.waitKey()




def parse_exif(file):
    content = file.read()
    offset = content.index(bytes.fromhex('FFE1'))
    file.seek(offset + 2)
    app1_data_size = file.read(2)
    print("APP1 data size:", int.from_bytes(app1_data_size, byteorder='little'))
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
    exif_offset, last_entry_adrress_ifd0 = read_entries(file, byte_align)

    print("METADATA FROM EXIF_SUBIFD:")
    file.seek(exif_offset+12)
    read_entries(file, byte_align)

    print("METADATA FROM IFD1:")
    file.seek(last_entry_adrress_ifd0)
    offset = file.read(4)
    offset = int.from_bytes(offset, byteorder=byte_align)
    file.seek(offset + 12)
    read_entries(file, byte_align)




def read_entries(file, byte_align):
    number_entries = file.read(2)
    number_entries = int.from_bytes(number_entries, byte_align)
    start_first_entry = file.tell()
    for entry in range(1, number_entries+1):
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

    

display_image()
DFT()
file = open('test.jpg', 'rb')
parse_exif(file)
file.close()

