import pickle
from CarChars import GetChars
from CarPlate import GetPlate 


def CarPlateRecognition(car_image, show):
    plate_like_objects = GetPlate(car_image, show)
    characters, column_list = GetChars(plate_like_objects, show)

    model = pickle.load(open('model00.bin', 'rb'))
    classification_result = []
    for each_character in characters:
        each_character = each_character.reshape(1, -1) 
        result = model.predict(each_character)
        classification_result.append(result)

    plate_string = ''
    for eachPredict in classification_result:
        plate_string += eachPredict[0]

    column_list_copy = column_list[:]
    column_list.sort()
    rightplate_string = ''
    for each in column_list:
        rightplate_string += plate_string[column_list_copy.index(each)]

    return rightplate_string



