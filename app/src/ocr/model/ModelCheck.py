# import os
import pickle
from skimage.filters import threshold_otsu
from skimage.io import imread


def check_img(img):
    img_details = img
    binary_image = img_details < threshold_otsu(img_details)
    flat_bin_image = binary_image.reshape(-1)

    model = pickle.load(open('model_big_rbf.bin', 'rb'))
    result = model.predict(flat_bin_image)
    return result

letter = 'c'
img_path = f"./data_train_big/{letter}/calibrili_upper.png"
img_details = imread(img_path, as_gray=True)

ch = check_img(img_details)
# model = pickle.load(open('model_big_rbf.bin', 'rb'))
