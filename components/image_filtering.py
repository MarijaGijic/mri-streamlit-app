import cv2
import numpy as np

def filter_image(images, filter_method = 'non_local_means', **kwargs):
    denoised_images = []

    for img in images:
        if filter_method == 'non_local_means':
            denoised_img = cv2.fastNlMeansDenoising(img, None, h=10, templateWindowSize=7, searchWindowSize=21)

        elif filter_method == 'gaussian':
            kernel_size = kwargs.get('kernel_size', (5, 5))
            std_dev_xy = kwargs.get('std_dev_xy', 0)
            denoised_img = cv2.GaussianBlur(img, kernel_size, std_dev_xy)

        elif filter_method == 'median':
            kernel_size = kwargs.get('kernel_size', 5)
            denoised_img = cv2.medianBlur(img, kernel_size)

        else:
            raise ValueError("Nepoznati metod za filtiranje")
        
        denoised_images.append(denoised_img)
    
    return denoised_images

