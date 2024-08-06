import cv2
import numpy as np
from skimage import morphology
from skimage.restoration import estimate_sigma, denoise_nl_means
from skimage import img_as_ubyte
from scipy.ndimage import gaussian_filter

def filter_image(img, filter_method):
    if filter_method == 'Original':
        return img
    if filter_method == 'Denoise':
        filtered_image = denoise_nl_means(img)
        return filtered_image

def denoise_nl_means(img):
    sigma_est = np.mean(estimate_sigma(img, channel_axis=None))
    denoise = denoise_nl_means(img, h=1.15 * sigma_est, sigma = sigma_est, fast_mode=True, patch_size=5, patch_distance=3)
    denoise_ubyte = img_as_ubyte(denoise)
    return denoise_ubyte

