import cv2
import numpy as np


car_cascade = cv2.CascadeClassifier("haarcascade_russian_plate_number.xml")
# https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml

cap = cv2.VideoCapture('license_plate.mp4')
# cap = cv2.VideoCapture('testvideo.mp4')
# cap = cv2.VideoCapture('cars.mp4')
# cap = cv2.VideoCapture('input.mp4')
# i = 0
while True: 
    ret, frames = cap.read()
    gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)
    cars = car_cascade.detectMultiScale(gray, 1.1, 9)
    # if str(np.array(cars).shape[0]) == '1':   # підрахунок кількості автомобілів на екрані
        # i += 1
        # continue
    for (x,y,w,h) in cars:
        plate = frames[y:y + h, x:x + w]
        cv2.rectangle(frames,(x,y),(x +w, y +h) ,(51 ,51,255),2)
        cv2.rectangle(frames, (x, y - 40), (x + w, y), (51,51,255), -2)
        cv2.putText(frames, 'Car', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.imshow('car', plate)

        # cv2.imwrite('car_plate.png', plate)       # постійний запис 'car_plate.png'
        if cv2.waitKey(1) & 0xFF == ord('s'):      # запис 'car_plate_crop.png' після натискання кнопки 
            cv2.imwrite('car_plate_crop.png', plate)

    # lab1 = f"Car Count: {i}"  # відображення кількості підрахованих автомобілів на екрані
    # cv2.putText(frames, lab1, (40, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (147, 20, 255), 3)
    frames = cv2.resize(frames,(600,400))
    cv2.imshow('Car Detection System', frames)

    # if cv2.waitKey(40) & 0xFF == ord('q'):    # press 'q' to quit
    #     break
    if cv2.waitKey(40) & 0xff == 27:     # press 'ESC' to quit
        break

cap.release()
cv2.destroyAllWindows()
