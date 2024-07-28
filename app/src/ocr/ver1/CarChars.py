import numpy as np
from skimage.transform import resize
from skimage import measure
from skimage.measure import regionprops
import matplotlib.patches as patches
import matplotlib.pyplot as plt


def GetChars(plate_like_objects, show = False):
    license_plate = np.invert(plate_like_objects[0])
    labelled_plate = measure.label(license_plate)

    fig, ax1 = plt.subplots(1)
    ax1.imshow(license_plate, cmap="gray")

    min_height = 0.35*license_plate.shape[0]
    max_height = 0.60*license_plate.shape[0]
    min_width = 0.05*license_plate.shape[1]
    max_width = 0.15*license_plate.shape[1]
    character_dimensions = (min_height, max_height, min_width, max_width)

    characters = []
    counter=0
    column_list = []
    for regions in regionprops(labelled_plate):
        y0, x0, y1, x1 = regions.bbox
        region_height = y1 - y0
        region_width = x1 - x0

        # if  (min_height < region_height < max_height) and (min_width < region_width < max_width):
        if region_height > min_height and region_height < max_height and region_width > min_width and region_width < max_width:
            roi = license_plate[y0:y1, x0:x1]

            # draw a red bordered rectangle over the character.
            rect_border = patches.Rectangle((x0, y0), x1 - x0, y1 - y0, edgecolor="red", linewidth=2, fill=False)
            ax1.add_patch(rect_border)

            # resize the characters to 20X20 and then append each character into the characters list
            resized_char = resize(roi, (20, 20))
            characters.append(resized_char)

            # this is just to keep track of the arrangement of the characters
            column_list.append(x0)
    # print(characters)
    if show:
        plt.savefig('4.Car-Chars.png', bbox_inches = 'tight')
        plt.show()
    
    return characters, column_list


if __name__ == "__main__":
    GetChars('../data/whitecar.png', True)