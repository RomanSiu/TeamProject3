import os
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
from skimage.io import imread
from skimage.filters import threshold_otsu
import pickle


letters = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def read_data(training_directory):
    image_data = []
    target_data = []
    for l in letters:
        for i in range(10):
            image_path = os.path.join(training_directory, l, f"{l}_{i}.jpg")
            img_details = imread(image_path, as_gray=True)
            binary_image = img_details < threshold_otsu(img_details)
            flat_bin_image = binary_image.reshape(-1)
            image_data.append(flat_bin_image)
            target_data.append(l)

    return (np.array(image_data), np.array(target_data))

def save_accuracy(info):
    with open("models_accuracy.txt", 'a') as f:
        f.write(info)

def cross_validation(model, num_of_fold, train_data, train_label, kernel):
    accuracy_result = cross_val_score(model, train_data, train_label, cv=num_of_fold)
    info = f"\nCross Validation Result for kernel {kernel} {num_of_fold}-fold:" + str(accuracy_result * 100)
    print(info)
    save_accuracy(info)


print('reading data')
train_data_dir = './train_data'
image_data, target_data = read_data(train_data_dir)
print('OK reading data')

model_kernel = 'linear'       # kernel: 'linear', 'poly' or 'rbf'
svc_model = SVC(kernel=model_kernel, probability=True)
cross_validation(svc_model, 4, image_data, target_data, model_kernel)

print('training model')
svc_model.fit(image_data, target_data)

print("model saving")
filename = f'./model_{model_kernel}.bin'
pickle.dump(svc_model, open(filename, 'wb'))
print(f"OK saved as: {filename!r}")
