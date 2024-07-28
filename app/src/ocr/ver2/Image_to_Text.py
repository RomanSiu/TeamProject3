import pickle
import numpy as np
from skimage import measure
from skimage.filters import threshold_otsu
from skimage.transform import resize
from skimage.measure import label, regionprops
from skimage.morphology import closing, square

import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


def GetPlate(car_image):
    gray_car_image = car_image * 255
    threshold_value = threshold_otsu(gray_car_image)
    binary_car_image = gray_car_image > threshold_value
    label_image = label(binary_car_image)

    plate_dimensions = (0.03*label_image.shape[0], 0.08*label_image.shape[0], 0.15*label_image.shape[1], 0.3*label_image.shape[1])
    min_height, max_height, min_width, max_width = plate_dimensions
    plate_dimensions2 = (0.08*label_image.shape[0], 0.2*label_image.shape[0], 0.15*label_image.shape[1], 0.4*label_image.shape[1])

    plate_objects_cordinates = []
    plate_objects = []

    flag =0
    for region in regionprops(label_image):
        if region.area < 50: 
            continue
        min_row, min_col, max_row, max_col = region.bbox
        region_height = max_row - min_row
        region_width = max_col - min_col

        if (min_height <= region_height <= max_height) and (min_width <= region_width <= max_width) and (region_width > region_height):
            flag = 1
            plate_objects.append(binary_car_image[min_row:max_row, min_col:max_col])
            plate_objects_cordinates.append((min_row, min_col, max_row, max_col))

    if(flag==0):
        min_height, max_height, min_width, max_width = plate_dimensions2
        plate_objects_cordinates = []
        plate_objects = []

        for region in regionprops(label_image):
            if region.area < 50:
                continue
            min_row, min_col, max_row, max_col = region.bbox
            region_height = max_row - min_row
            region_width = max_col - min_col

            if (min_height <= region_height <= max_height) and (min_width <= region_width <= max_width) and (region_width > region_height):
                plate_objects.append(gray_car_image[min_row:max_row, min_col:max_col])
                plate_objects_cordinates.append((min_row, min_col, max_row, max_col))

    return  plate_objects


def GetChars(plate):
    thresh = threshold_otsu(plate)
    bw = closing(plate > thresh, square(3))
    # platei = 255 - bw
    platei = np.invert(bw)

    label_image = label(platei)

    min_height, max_height = 0.5*plate.shape[0], 0.98*plate.shape[0]
    min_width,  max_width  = 0.05*plate.shape[1], 0.15*plate.shape[1]

    characters = []
    column_list = []

    for r in regionprops(label_image):
        if r.area < 40: 
            continue
        y0, x0, y1, x1 = r.bbox
        region_height = y1 - y0
        region_width = x1 - x0

        if (min_height < region_height < max_height) and (min_width < region_width < max_width):
            roi = platei[y0:y1, x0:x1]
            resized_char = resize(roi, (20, 20))
            characters.append(resized_char)
            column_list.append(x0)
    
    return characters, column_list


def CarPlateRecognition(car_image):
    plate_objects = GetPlate(car_image)
    if len(plate_objects) == 0:
        return ''
    
    characters, column_list = GetChars(plate_objects[0])
    if len(characters) == 0:
        return ''

    model = pickle.load(open('model_linear.bin', 'rb'))
    char_pred = []
    for ch in characters:
        ch = ch.reshape(1, -1) 
        result = model.predict(ch)
        char_pred.append(result)

    plate_string = ''
    for pred in char_pred:
        plate_string += pred[0]

    column_list_copy = column_list[:]
    column_list.sort()
    rightplate_string = ''
    for each in column_list:
        rightplate_string += plate_string[column_list_copy.index(each)]

    return rightplate_string



if __name__ == "__main__":
    # швидка перевірка роботи модуля без запуску demo.py
    from skimage.io import imread

    car_image = imread('../data/09.jpg', as_gray=True)
    print(car_image.shape)

    text = CarPlateRecognition(car_image)
    print(text)
    