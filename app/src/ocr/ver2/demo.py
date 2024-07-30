import pickle

from skimage.io import imread
from skimage.measure import label, regionprops
from skimage.transform import resize

from app.src.ocr.ver2.Image_to_Text import GetPlate, GetChars


def demo(car_image):
    # image_path = '../data/09.jpg'  # <<< Input demo file
    # car_image = None
    #
    try:
        car_image = imread(car_image, as_gray=True)
    except:
        print(f'[ERROR] can"t read file: {car_image}')
        return

    plate_objects = GetPlate(car_image)
    print(f"[INFO] license plates found: {len(plate_objects)}")
    if len(plate_objects) == 0:
        print('[ERROR] 0 license plates found')
        return ''
    
    characters, column_list = GetChars(plate_objects[0])
    print(f"[INFO] characters found: {len(characters)}")
    if len(characters) == 0:
        print('[ERROR] 0 characters found')
        return ''
        
    model = pickle.load(open('app/src/ocr/ver2/model_linear.bin', 'rb'))
    # model = pickle.load(open('model02.bin', 'rb'))
    # model = pickle.load(open('model_poly.bin', 'rb'))
    # model = pickle.load(open('model_rbf.bin', 'rb'))
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

    if len(rightplate_string):
        print(f"[INFO] {len(rightplate_string)} characters were recognized")
        print(f'Number: {rightplate_string}')
        return rightplate_string
    else:
        print('[ERROR] can"t recognize any char')
