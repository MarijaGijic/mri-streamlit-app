import cv2
import numpy as np

def contrast_enhancement(images, method = 'clahe', **kwargs):
    enhanced_images = []

    for img in images:
        if method == 'clahe':
            clip_limit = kwargs.get('clip_limit', 2.0)
            tile_grid_size = kwargs.get('tile_grid_size', (8, 8))
            clahe = cv2.createCLAHE(clipLimit = clip_limit, tileGridSize = tile_grid_size)
            enhanced_img = clahe.apply(img)

        elif method == 'gamma':
            gamma = kwargs.get('gamma', 1.0)
            inv_gamma = 1.0 / gamma
            table = np.array([i / 255.0 ** inv_gamma * 255 for i in np.arange(0.256)]).astype("uint8")
            enhanced_img = cv2.LUT(img, table)

        elif method == 'unsharp':
            sigma = kwargs.get('sigma', 1.0)
            strength = kwargs.get('strength', 1.5)
            kernel_size = kwargs.get('kernel_size', (0, 0))
            blurred_img = cv2.GaussianBlur(img, kernel_size, sigma)
            enhanced_img = cv2.addWeighted(img, 1 + strength, blurred_img, -strength, 0)

        else:
            raise ValueError("Nepostojeci metod")
        
        enhanced_images.append(enhanced_img)

    return enhanced_images