import pickle

import numpy as np
import cv2
from skimage.measure import regionprops, label
from skimage.transform import resize
from skimage.segmentation import clear_border
from skimage.measure import label, regionprops


def model_load(name):
    model = pickle.load(open(name, 'rb'))
    # model = pickle.load(open('model_big6_rbf.bin', 'rb'))
    w = pickle.load(open('app/src/ocr/ver3/model_w.bin', 'rb'))
    return w


def image2plate(car_image):
    median_image = cv2.medianBlur(car_image, 5)
    gray = cv2.cvtColor(median_image, cv2.COLOR_BGR2GRAY)
    bin_image = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)[1]
    label_image = label(bin_image)

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
            plate_objects.append(bin_image[min_row:max_row, min_col:max_col])
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
                plate_objects.append(bin_image[min_row:max_row, min_col:max_col])
                plate_objects_cordinates.append((min_row, min_col, max_row, max_col))

    return  plate_objects   # , plate_objects_cordinates


def check_weights(img, ww):
    w = (ww[img] if img in ww else '')
    return (w if w else "weights are not defined")


def plate2char(plate_image):
    imagei = np.invert(plate_image)
    plate = clear_border(imagei)    # plate == cleared bordure

    label_image = label(plate)
    regions = [region for region in regionprops(label_image)]

    # character_dimensions = (0.35*plate.shape[0], 0.60*plate.shape[0], 0.05*plate.shape[1], 0.15*plate.shape[1])
    # min_height, max_height, min_width, max_width = character_dimensions
    min_height, max_height = 0.5*plate.shape[0], 0.98*plate.shape[0]
    min_width,  max_width  = 0.05*plate.shape[1], 0.15*plate.shape[1]

    characters = []
    column_list = []    
    for r in regions:
        if r.area < 50: 
            continue
        y0, x0, y1, x1 = r.bbox
        region_height = y1 - y0
        region_width = x1 - x0

        if (min_height < region_height < max_height) and (min_width < region_width < max_width):  
            roi = plate[y0:y1, x0:x1]
            resized_char = resize(roi, (20, 20))
            characters.append(resized_char)
            column_list.append(x0)

    return characters, column_list


def image2text(car_image, model):

    plates = image2plate(car_image)
    if len(plates) == 0:
        # print('[ERROR] can"t find any car license plate')
        return ''
    
    characters, column_list = plate2char(plates[0])
    if len(characters) == 0:
        # print('[ERROR] can"t find any char')
        return ''

    char_pred = []
    for i in range(len(characters)):
        ch_f = characters[i].reshape(1, -1) 
        result = model.predict(ch_f)[0]
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


def main(car_image):
    model = model_load('app/src/ocr/ver3/model_rbf.bin')
    check = check_weights(car_image, model)
    return check


#CALL:  car_number = main(short_filename_for_car_image)
