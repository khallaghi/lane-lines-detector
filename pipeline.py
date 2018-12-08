import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import math
import helper_funcs as helper
import extrapolate 
import os


def process_image(image):
    # make image gray
    gray_img = helper.grayscale(image)

    # apply  Gaussian blur 
    gauss_img = helper.gaussian_blur(gray_img, 3)

    # apply Canny transform
    canny_img = helper.canny(gauss_img, 100, 200)

    # cut out a triangle from image 
    plygn_verts = np.array([[
        [image.shape[1]/2, image.shape[0]/2],
        [image.shape[1], image.shape[0]],
        [0, image.shape[0]]
    ]], dtype=np.int32) 
    roi_img = helper.region_of_interest(canny_img, plygn_verts)

    # apply hough line detector
    line_img, lines = helper.hough_lines(roi_img, 1, np.pi/180, 50, 20, 10)

    # extrapolate and average detected lines and apply the new main line on image
    overlay_img = extrapolate.draw_lane_lines(image, extrapolate.lane_lines(image, lines))

    # return result 
    return overlay_img

def pipeline(img_addr, result_dir):
    image = mpimg.imread(img_addr)
    print('This image is:', type(image), 'with dimensions:', image.shape)
    final_img = process_image(image)
    mpimg.imsave(os.path.join(result_dir, os.path.basename(img_addr)), final_img)

    # show the result
    # plt.imshow(final_img, cmap='gray') 
    # plt.show()

