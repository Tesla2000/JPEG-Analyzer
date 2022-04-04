import cv2 as cv
import sys
import numpy as np


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

    # cv.imshow("spectrum magnitude", amplitude_spectrum)
    # cv.waitKey()


display_image()
DFT()

