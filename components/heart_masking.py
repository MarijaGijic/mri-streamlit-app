import cv2
import numpy as np
from image_contrast_enhancement import contrast_enhancement

def apply_watershed(images, roi_images, roi_box, **kwargs):

    enhanced_images = contrast_enhancement(roi_images, 'gamma', gamma = 2.5)
    masks = []
    kernel = kwargs.get('kernel', (5, 5))
    kernel = np.ones(kernel, np.uint8)
    x, y, w, h = roi_box

    for img, roi in zip(images, enhanced_images):
        _, thresh = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations = 1)

        sure_bg = cv2.dilate(opening, kernel, iterations = 2)
        dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 3)
        _, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
        sure_fg = np.uint8(sure_fg)
        sure_fg = cv2.dilate(sure_fg, np.ones((9, 9), np.uint8), iterations = 3)
        unknown = cv2.subtract(sure_bg, sure_fg)

        _, markers = cv2.connectedComponents(np.uint8(sure_fg))
        markers = markers + 1
        markers[unknown == 255] = 0
        markers = np.int32(markers)

        if len(roi.shape) == 2:
            roi = cv2.cvtColor(roi, cv2.COLOR_GRAY2BGR)

        markers = cv2.watershed(roi, markers)

        mask = np.zeros_like(roi, dtype = np.uint8)
        mask[markers != 1] = [255, 255, 255]
        mask_gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

        mask_resized = np.zeros_like(img, dtype = np.uint8)
        mask_resized[y:y+h, x:x+w] = mask_gray

        masked_img = img.copy()
        masked_img[mask_resized == 255] = 0

        masks.append(masked_img)

    return masks

