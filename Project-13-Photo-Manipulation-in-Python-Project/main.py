import cv2
import numpy as np


image = cv2.imread('image.jpg')

if image is None:
    print("❌ Error: Could not load image. Please check the file path.")
    exit()

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

edges = cv2.Canny(gray_image, 50, 150)

cv2.imshow('Original Image', image)
cv2.imshow('Grayscale Image', gray_image)
cv2.imshow('Edge Detection', edges)

cv2.waitKey(0)
cv2.destroyAllWindows()
