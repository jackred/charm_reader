import os
import numpy as np
from skimage.color import rgb2gray
from PIL import Image


# dict keep insertion order
def load(folder, gray=True):
    list_elem = os.listdir(folder)
    elems = {}
    for i in list_elem:
        if i[-4:] == '.png':
            tmp = np.array(Image.open(folder+'/'+i).convert('RGB'))
            if gray:
                tmp = rgb2gray(tmp)
            else:
                tmp = tmp/255
            elems[i[:-4].replace('_', '/')] = tmp
    return elems


def load_skills(folder='./skills'):
    return load(folder)


def load_values(folder='./values'):
    return load(folder)


def load_rarities(folder='./rarities'):
    return load(folder, False)


def load_slots(folder='./slots'):
    return load(folder)


def load_data():
    data = {}
    data['skills'] = load_skills()
    data['values'] = load_values()
    data['rarities'] = load_rarities()
    data['slots'] = load_slots()
    data['skills_name'] = np.array(list(data['skills']))
    data['values_name'] = np.array(list(data['values']))
    data['rarities_name'] = np.array(list(data['rarities']))
    data['slots_name'] = np.array(list(data['slots']))
    return data
