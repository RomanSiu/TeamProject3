# License Plate Detection Project
Версія 2

## ModelTrain.py
- Модуль для тренування моделі та запису ії у файл:
    - ``model_linear.bin``: SVC kernel = 'linear'
    - ``model_poly.bin``: SVC kernel = 'poly'
    - ``model_rbf.bin``: SVC kernel = 'rbf'
      
    Показники моделей (Cross Validation Result) збережені у файлі ``models_accuracy.txt``
    Використувались навчальні файли з буквами і цифрами (на git не завантажені)

## Image_to_Text.py
- Основний модуль з функцією розпізнавання номерних знаків авто.
    - Використання: car_number = **Image_to_Text.CarPlateRecognition(car_image)**
    - Input: car_image (у форматі .jpeg, .jpg або .png)
    - Output: string
- За замовченням використовується модель ``model_linear.bin``

## demo.py
- Приклад використання модуля **Image_to_Text.py**
