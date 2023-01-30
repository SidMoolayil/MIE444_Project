import cv2
import numpy as np

def kmeans_color_quantization(image, clusters=3, rounds=1):
    h, w = image.shape[:2]
    samples = np.zeros([h*w,3], dtype=np.float32)
    count = 0

    for x in range(h):
        for y in range(w):
            samples[count] = image[x][y]
            count += 1

    compactness, labels, centers = cv2.kmeans(samples,
            clusters,
            None,
            (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10000, 0.0001),
            rounds,
            cv2.KMEANS_RANDOM_CENTERS)

    centers = np.uint8(centers)
    res = centers[labels.flatten()]
    return res.reshape((image.shape))

if __name__ == "__main__":
    image_path = "/Users/sidhanthmoolayil/Desktop/MIE444_Code/IMG_8153.jpg"
    image = cv2.imread(image_path)
    image = cv2.resize(image, [150, 150])
    result = kmeans_color_quantization(image, clusters=4)
    result = kmeans_color_quantization(result, clusters=3)
    cv2.imshow('result', result)
    cv2.waitKey()