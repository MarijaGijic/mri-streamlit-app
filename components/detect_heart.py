import numpy as np

def detect_heart_based_on_roi(images, roi_box, threshold = 45):
    results = []
    avg_intensity_ = []
    x, y, w, h = roi_box

    for img in images:
        roi = img[y:y+h, x:x+w]
        avg_intensity = np.mean(roi)

        heart_visible = avg_intensity > threshold
        results.append(heart_visible)
        avg_intensity_.append(avg_intensity)

    return results, avg_intensity_


    
