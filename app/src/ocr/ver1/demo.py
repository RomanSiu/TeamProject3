from skimage.io import imread
from NumberRecognition import CarPlateRecognition 


def demo():
    try:
        image_path = '../data/whitecar.png'
        car_image = imread(image_path, as_gray=True)
        plate_number = CarPlateRecognition(car_image, show = True)
    except:
        plate_number = "-- unknown --"
    print(f' >> Image path: {image_path}\n >> License plate: {plate_number}')


if __name__ == "__main__":
    demo()

