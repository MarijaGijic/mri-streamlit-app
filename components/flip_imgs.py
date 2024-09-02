# Vertical flip
import cv2

def flip_imgs(images):
    flipped_images = []
    for img in images:
        flipped_img = cv2.flip(img, 0)
        flipped_images.append(flipped_img)

    return flipped_images