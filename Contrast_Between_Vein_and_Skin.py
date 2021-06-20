import cv2
import matplotlib.pyplot as MPL
import numpy as np

# image = cv2.imread("D:/Capstone Project/anh do an/anh canh tay/2021-06-11_23-07-42.jpg")
# MPL.imshow(image, cmap=MPL.cm.gray, interpolation='nearest')
# MPL.show()

# a = np.linspace(45,90, 1)
# locs = np.where(image == a)
# # pixels = image[locs]
# Uvein = np.mean(locs)
# print(Uvein)

# b = np.linspace(100, 165, 1)
# locs1 = np.where(image == b)
# # pixels = image[locs]
# Uskin = np.mean(locs1)
# print(Uskin)

# ảnh sẽ được cắt thành 1 phần nhỏ (ROI) từ ảnh xám để lấy được vùng trung bình của tĩnh mạch
imagevein = cv2.imread("Your path")
# ảnh sẽ được cắt thành 1 phần nhỏ (ROI) từ ảnh xám để lấy được vùng trung bình của da
imageskin = cv2.imread("Your path")
cv2.imshow('vein', imagevein)
cv2.waitKey(0)
cv2.imshow('skin', imageskin)
cv2.waitKey(0)

Uvein = np.mean(imagevein)
Uskin = np.mean(imageskin)

M = np.abs(Uvein - Uskin)/(Uvein + Uskin)
print(M)
