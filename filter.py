import cv2
import numpy as np

def gray_img(path):
    img_src = cv2.imread(cv2.samples.findFile(path))
    img_src = cv2.equalizeHist(cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY))

    return img_src

def average_filter(img, size = 5):
    return cv2.blur(img,(size,size))

def gaussian_filter(img, size = 5):
    return cv2.GaussianBlur(img,(size,size),0)

def hight_pass_filter(img):
    kernel_hight_pass = np.array([[-1, -1, -1.0], 
                                [-1, 8, -1],
                                [-1, -1, -1.0]])

    kernel_hight_pass = np.array([[0, -1, 0], 
                                [-1, 5, -1],
                                [0, -1, 0]])

    img_res = cv2.filter2D(img,-1,kernel_hight_pass)

    return img_res
    
def sharpening(img):
    kernel_hight_pass = np.array([[0, -1, 0], 
                                [-1, 5, -1],
                                [0, -1, 0]])

    img_res = cv2.filter2D(img,-1,kernel_hight_pass)

    return img_res

def horizontal_edge_detect(img):
    kernel_horizontal_edge = np.array([[1, 2, 1],
                                [0, 0, 0],
                                [-1, -2, -1]])

    img_horizontal_edge = cv2.filter2D(img,-1,kernel_horizontal_edge)

    return img_horizontal_edge

def vertical_edge_detect(img):
    kernel_vertical_edge = np.array([[1, 0, -1.0], 
                                [2.0, 0, -2.0],
                                [1.0, 0, -1.0]])

    img_vertical_edge = cv2.filter2D(img,-1,kernel_vertical_edge)

    return img_vertical_edge