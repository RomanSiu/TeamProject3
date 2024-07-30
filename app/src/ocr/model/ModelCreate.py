import os
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
from skimage.io import imread
from skimage.filters import threshold_otsu
import pickle


letters = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


def fill_data(data_directory):
    image_data = []
    target_data = []
    print(data_directory)

    for l in letters:
        letter_dir = os.listdir(os.path.join(data_directory, l))
        for i in letter_dir:
            tmp = os.path.join(data_directory, l, i)
            img_details = imread(tmp, as_gray=True)
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
    info = f"\n(big) Cross Validation Result for kernel {kernel!r}:{num_of_fold}-fold: {accuracy_result * 100}"
    print(info)
    save_accuracy(info)


# print('reading data from data directory: "./data_train_big/" ...')
# image_data, target_data = fill_data('./data_train_big/')

print('reading data from .bin files ...')
image_data = pickle.load(open("image_data.bin", 'rb'))
target_data = pickle.load(open("target_data.bin", 'rb'))

print('OK reading data')
print(f"image_data: {len(image_data)} items")
print(f"target_data: {len(target_data)} items")

print('\ntraining model')
model_kernel = 'rbf'       # kernel: 'linear', 'poly' or 'rbf'
svc_model = SVC(kernel=model_kernel, probability=True)
cross_validation(svc_model, 6, image_data, target_data, model_kernel)
svc_model.fit(image_data, target_data)

print("model saving ...")
filename = f'./model_big6_{model_kernel}.bin'
pickle.dump(svc_model, open(filename, 'wb'))
print(f"OK, saved as: {filename!r}")

ddict = {
    

}

# pickle.dump(image_data, open("image_data.bin", 'wb'))
# pickle.dump(target_data, open("target_data.bin", 'wb'))
