import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2
from skimage.color import rgb2gray
from skimage.transform import resize
import os
from PIL import Image


# need to clean code
th_slot = 20
th_skill = 70
th_value = 13
th_rarity = 40

threshold = {'rarity': th_rarity, 'skill_1': th_skill, 'value_1': th_value,
             'skill_2': th_skill, 'value_2': th_value, 'slot_1': th_slot,
             'slot_2': th_slot, 'slot_3': th_slot}

shape = (720, 1280, 3)

x_range = range(750, 990)
y_range = range(190, 375)

rarity_x = range(180, 239)
rarity_y = range(3, 22)

slot_y = range(23, 47)

slot_1_x = range(154, 181)  # 26
slot_2_x = range(182, 209)  # 27
slot_3_x = range(210, 237)  # 27

skill_x = range(23, 174)
skill_1_y = range(89, 108)
skill_2_y = range(140, 159)

value_x = range(228, 236)
value_1_y = range(116, 131)
value_2_y = range(166, 181)

index = ['rarity', 'skill_1', 'value_1', 'skill_2',
         'value_2', 'slot_1', 'slot_2', 'slot_3']


def get_sub_frame(frame, x, y):
    return frame[y][:, x]


def get_rarity(frame):
    return get_sub_frame(frame, rarity_x, rarity_y)


def get_slot_1(frame):
    return get_sub_frame(frame, slot_1_x, slot_y)


def get_slot_2(frame):
    return get_sub_frame(frame, slot_2_x, slot_y)


def get_slot_3(frame):
    return get_sub_frame(frame, slot_3_x, slot_y)


def get_skill_1(frame):
    return get_sub_frame(frame, skill_x, skill_1_y)


def get_skill_2(frame):
    return get_sub_frame(frame, skill_x, skill_2_y)


def get_value_1(frame):
    return get_sub_frame(frame, value_x, value_1_y)


def get_value_2(frame):
    return get_sub_frame(frame, value_x, value_2_y)


def get_charm_sub_frame(frame):
    return get_sub_frame(frame, x_range, y_range)


def is_different(f1, f2):
    return ((f1 == f2).sum()/f1.size) < 0.80


def calculateDistance(i1, i2):
    return np.sum((i1-i2)**2)


def process_image(image):
    image = image[:, :, ::-1]
    image = resize(image, shape)
    return image


def extract_frames(video):
    not_stop, frame = video.read()
    frame = process_image(frame)
    res = []
    if not_stop:
        tmp = get_charm_sub_frame(frame)
        res.append(tmp)
        fp = tmp
        while(not_stop):
            not_stop, frame = video.read()
            if not_stop:
                frame = process_image(frame)
                tmp = get_charm_sub_frame(frame)
                if calculateDistance(tmp, fp) > 30:
                    res.append(tmp)
                    fp = tmp
    return res


def same_infos(i1, i2):
    return all([calculateDistance(i1[i], i2[i]) < threshold[i]
                for i in i2])


# to clean
def read_frames(video, data):
    not_stop, frame = video.read()
    frame = process_image(frame)
    res = pd.DataFrame(columns=index)
    if not_stop:
        tmp = get_charm_sub_frame(frame)
        infos = get_all_infos(tmp)
        reading = read_infos_charm(infos, data)
        if not (reading == '').all():
            # kinda useless to index in reading before but eh
            res = res.append(reading, ignore_index=True)
        while(not_stop):
            not_stop, frame = video.read()
            if not_stop:
                frame = process_image(frame)
                tmp = get_charm_sub_frame(frame)
                infos = get_all_infos(tmp)
                reading = read_infos_charm(infos, data)
                if not (reading == '').all() \
                   and (len(res) == 0
                        or not ((reading == res.iloc[-1]).all())):
                    res = res.append(reading, ignore_index=True)
    return res


def read_video(filename, data):
    cap = cv2.VideoCapture(filename)
    return read_frames(cap, data)


def read_videos(folder_name):
    data = load_data()
    files = os.listdir(folder_name)
    res = pd.DataFrame(columns=index)
    for i in files:
        if i[-4:] == '.mp4':
            res = res.append(read_video(folder_name + '/' + i, data))
    return res


def read_videos_store_csv(folder_name):
    charms = read_videos(folder_name)
    save_csv(charms, folder_name + '/output.csv')


def get_all_infos(frame):
    res = {}
    res['slot_1'] = rgb2gray(get_slot_1(frame))
    res['slot_2'] = rgb2gray(get_slot_2(frame))
    res['slot_3'] = rgb2gray(get_slot_3(frame))
    res['skill_1'] = rgb2gray(get_skill_1(frame))
    res['skill_2'] = rgb2gray(get_skill_2(frame))
    res['rarity'] = get_rarity(frame)
    res['value_1'] = rgb2gray(get_value_1(frame))
    res['value_2'] = rgb2gray(get_value_2(frame))
    return res


def show(f, cmap=None):
    plt.imshow(f, cmap=cmap)
    plt.show(block=False)


def find_proba(element, list_name):
    return np.array([calculateDistance(element, e)
                     for e in list_name.values()])


def get_index(ele, threshold):
    return np.where(ele < threshold)[0]


def link_element(id_e, list_name, th, threshold, i=0):
    if len(id_e) == 1:
        return list_name[id_e[0]]
    elif len(id_e) == 0:
        return ''
    else:
        if i < 3:
            id_e = get_index(th, threshold/2)
            return link_element(id_e, list_name, th, threshold/2, i+1)
        else:
            return 'Multiple match found:' + ' '.join(list_name[id_e])


def read_info(elem, list_elem, list_elem_name, threshold):
    th = find_proba(elem, list_elem)
    id_e = get_index(th, threshold)
    return link_element(id_e, list_elem_name, th, threshold)


def read_slot_charm(elem, list_elem, list_elem_name):
    return read_info(elem, list_elem, list_elem_name, th_slot)


def read_rarity_charm(elem, list_elem, list_elem_name):
    return read_info(elem, list_elem, list_elem_name, th_rarity)


def read_value_charm(elem, list_elem, list_elem_name):
    return read_info(elem, list_elem, list_elem_name, th_value)


def read_skill_charm(elem, list_elem, list_elem_name):
    return read_info(elem, list_elem, list_elem_name, th_skill)


def read_infos_charm(infos, data):
    res = pd.Series(index=index, dtype=str)
    res['rarity'] = read_rarity_charm(
        infos['rarity'], data['rarities'], data['rarities_name'])
    res['skill_1'] = read_skill_charm(
        infos['skill_1'], data['skills'], data['skills_name'])
    res['value_1'] = read_value_charm(
        infos['value_1'], data['values'], data['values_name'])
    res['skill_2'] = read_skill_charm(
        infos['skill_2'], data['skills'], data['skills_name'])
    res['value_2'] = read_value_charm(
        infos['value_2'], data['values'], data['values_name'])
    res['slot_1'] = read_value_charm(
        infos['slot_1'], data['slots'], data['slots_name'])
    res['slot_2'] = read_value_charm(
        infos['slot_2'], data['slots'], data['slots_name'])
    res['slot_3'] = read_value_charm(
        infos['slot_3'], data['slots'], data['slots_name'])
    return res


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


def save(title, image, folder, cmap='gray'):
    plt.imsave('./%s/%s.png' % (folder, title), image, cmap=cmap)


def save_skill(title, image):
    save(title, image, 'skills')


def save_rarity(title, image):
    save(title, image, 'rarities', None)


def save_value(title, image):
    save(title, image, 'values')


def save_slot(title, image):
    save(title, image, 'slots')


def save_csv(charms, name):
    charms['mix'] = (charms['skill_1'] + ' ' + charms['value_1'] + ' '
                     + charms['skill_2'] + ' ' + charms['value_2']).str.strip()
    charms['slots'] = (charms['slot_1'] + '-' + charms['slot_2']
                       + '-' + charms['slot_3'])
    charms = charms[['skill_1', 'value_1', 'skill_2',
                     'value_2', 'mix', 'slots']]
    charms.to_csv(name, index=False)
