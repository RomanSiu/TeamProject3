import os
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
from skimage.io import imread
from skimage.filters import threshold_otsu
import pickle


letters = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def read_training_data(training_directory):
    image_data = []
    target_data = []
    for each_letter in letters:
        for each in range(10):
            image_path = os.path.join(training_directory, each_letter, each_letter + '_' + str(each) + '.jpg')
            img_details = imread(image_path, as_gray=True)
            binary_image = img_details < threshold_otsu(img_details)
            flat_bin_image = binary_image.reshape(-1)
            image_data.append(flat_bin_image)
            target_data.append(each_letter)

    return (np.array(image_data), np.array(target_data))

def cross_validation(model, num_of_fold, train_data, train_label):
    accuracy_result = cross_val_score(model, train_data, train_label, cv=num_of_fold)
    print("Cross Validation Result for ", str(num_of_fold), " -fold")
    print(accuracy_result * 100)

print('reading data')
training_dataset_dir = './chars20X20'
image_data, target_data = read_training_data(training_dataset_dir)
print('OK reading data')

# kernel: 'linear', 'poly' or 'rbf'
svc_model = SVC(kernel='rbf', probability=True)
cross_validation(svc_model, 4, image_data, target_data)
print('training model')
svc_model.fit(image_data, target_data)

print("model saving")
filename = './model00.bin'
pickle.dump(svc_model, open(filename, 'wb'))
print(f"OK: {filename!r}")
