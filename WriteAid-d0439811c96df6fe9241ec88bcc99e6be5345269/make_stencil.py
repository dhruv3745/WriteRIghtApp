import cv2
import os
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

def img2sketch(photo, k_size):
    #Read Image
    img=cv2.imread(photo)
    
    # Convert to Grey Image
    grey_img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Invert Image
    invert_img=cv2.bitwise_not(grey_img)
    #invert_img=255-grey_img

    # Blur image
    blur_img=cv2.GaussianBlur(invert_img, (k_size,k_size),0)

    # Invert Blurred Image
    invblur_img=cv2.bitwise_not(blur_img)
    #invblur_img=255-blur_img

    # Sketch Image
    sketch_img=cv2.divide(grey_img,invblur_img, scale=256.0)
    image_bgr = cv2.cvtColor(sketch_img,cv2.COLOR_GRAY2RGB)
    #Make White Transparent
    h, w, c = image_bgr.shape
    # append Alpha channel -- required for BGRA (Blue, Green, Red, Alpha)
    image_bgra = np.concatenate([image_bgr, np.full((h, w, 1), 255, dtype=np.uint8)], axis=-1)
    # create a mask where white pixels ([255, 255, 255]) are True
    white = np.all(image_bgr == [255, 255, 255], axis=-1)
    # change the values of Alpha to 0 for all the white pixels
    image_bgra[white, -1] = 0
    

    # Save Sketch 
    cv2.imwrite('sketch.png', image_bgra)

    # Display sketch
    #cv2.imshow('sketch image',image_bgra)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    
#Function call
image_path = 'original.png'
img2sketch(photo= image_path, k_size=7)
