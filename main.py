import numpy as np
import matplotlib.pyplot as plt
import cv2
from skimage.color import rgb2gray
from skimage.transform import resize
import os
from PIL import Image
from math import floor

cap = cv2.VideoCapture('data/video_2021-05-04_07-33-58.mp4')
cap2 = cv2.VideoCapture('data/50mystery.mp4')
cap3 = cv2.VideoCapture('data/charm.mp4')
cap4 = cv2.VideoCapture('data/mysterywithkagero.mp4')

ret, frame = cap.read()
plt.imshow(frame)
plt.show()

shape = (720, 1280, 3)

x_range = range(750, 990)
y_range = range(190, 375)

rarity_x = range(180, 239)
rarity_y = range(3, 22)

slot_x = range(150, 239)
slot_y = range(23, 47)

skill_x = range(23, 174)
skill_1_y = range(89, 108)
skill_2_y = range(140, 159)

value_x = range(228, 236)
value_1_y = range(116, 131)
value_2_y = range(166, 181)


def get_sub_frame(frame, x, y):
    return frame[y][:, x]


def get_rarity(frame):
    return get_sub_frame(frame, rarity_x, rarity_y)


def get_slot(frame):
    return get_sub_frame(frame, slot_x, slot_y)


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


def process_image(image):
    image = image[:, :, ::-1]
    image = resize(image, shape)
    #image = rgb2gray(image)
    return image


def extract_frames(video):
    not_stop, frame = video.read()
    frame = process_image(frame)
    res = []
    if not_stop:
        res.append(get_charm_sub_frame(frame))
        while(not_stop):
            not_stop, frame = video.read()
            if not_stop:
                frame = process_image(frame)
                tmp = get_charm_sub_frame(frame)
                if is_different(res[-1], tmp):
                    res.append(tmp)
    return res


def get_all_infos(frame):
    res = {}
    res['slot'] = rgb2gray(get_slot(frame))
    res['skill_1'] = rgb2gray(get_skill_1(frame))
    res['skill_2'] = rgb2gray(get_skill_2(frame))
    res['rarity'] = get_rarity(frame)
    res['value_1'] = rgb2gray(get_value_1(frame))
    res['value_2'] = rgb2gray(get_value_2(frame))
    return res


def plot_infos(infos):
    length = int(len(infos)/2)
    fig, axs = plt.subplots(length, 2)
    for i, k in enumerate(infos):
        axs[i % length][floor(i/length)].imshow(infos[k])
        axs[i % length][floor(i/length)].set_title(k)


def plot_frame_infos(frame):
    infos = get_all_infos(frame)
    plot_infos(infos)
    plt.show()


def show(f, cmap=None):
    plt.imshow(f, cmap=cmap)
    plt.show(block=False)



thr = 50  
def calculateDistance(i1, i2):
    return np.sum((i1-i2)**2)

# same as below, but less time
def find_proba_skill(s1, s2, skills):
    dist_s1 = []
    dist_s2 = []
    for j in skills:
        dist_s1.append(calculateDistance(s1, skills[j]))
        dist_s2.append(calculateDistance(s2, skills[j]))
    return np.array(dist_s1), np.array(dist_s2)

def find_proba(element, list_name):
    return np.array([calculateDistance(element, e) for e in list_name.values()])

# use get_index, too lazy to do rn
# even tho it prolly took me longer to write this comment
# than to do it
def get_indexs(s1, s2, threshold=70):
    return np.where(s1 < threshold)[0], np.where(s2 < threshold)[0]

def get_index(ele, threshold):
    return np.where(ele < threshold)[0]

def link_element(id_e, list_name):
    if len(id_e) == 1:
        return list_name[id_e[0]]
    elif len(id_e) == 0:
        return ''
    else:
        return 'Multiple match found:' + ' '.join(list_name[id_e])


def read_skill_charm(s1, s2, skills, skills_name):
    th_1, th_2 = find_proba_skill(s1, s2, skills)
    id_s1, id_s2 = get_indexs(th_1, th_2, 70)
    return link_element(id_s1, skills_name), link_element(id_s2, skills_name)

def read_rarity_charm(r, raritys, raritys_name):
    th = find_proba(r, raritys)
    id_r = get_index(th, 40)
    return link_element(id_r, raritys_name)

# litterally the same function
# todo: only one
# again lazy rn
def read_value_charm(v, values, values_name):
    th = find_proba(v, values)
    id_v = get_index(th, 10)
    return link_element(id_v, values_name)

def read_infos_charm(infos, skills, skills_name, raritys, raritys_name,
                     values, values_name):
    res = {}
    res['rarity'] = read_rarity_charm(infos['rarity'], raritys, raritys_name)
    res['skill_1'], res['skill_2'] = read_skill_charm(
        infos['skill_1'], infos['skill_2'], skills, skills_name)
    res['value_1'] = read_value_charm(infos['value_1'], values, values_name)
    res['value_2'] = read_value_charm(infos['value_2'], values, values_name)
    return res

# same as all, make only one function
# dict keep insertion order
def load_skills(folder='./skills'):
    list_skill = os.listdir(folder)
    skills = {}
    for i in list_skill:
        if i[-4:] == '.png':
            skills[i[:-4].replace('_', '/')] = rgb2gray(np.array(
                Image.open(folder+'/'+i).convert('RGB')))
    return skills

# dict keep insertion order
def load_values(folder='./value'):
    list_value = os.listdir(folder)
    value = {}
    for i in list_value:
        if i[-4:] == '.png':
            value[i[:-4].replace('_', '/')] = rgb2gray(np.array(
                Image.open(folder+'/'+i).convert('RGB')))
    return value


# dict keep insertion orer
def load_raritys(folder='./rarity'):
    list_rarity = os.listdir(folder)
    raritys = {}
    for i in list_rarity:
        if i[-4:] == '.png':
            raritys[i[:-4]] = np.array(
                Image.open(folder+'/'+i).convert('RGB')) / 255
    return raritys




def save_skills(title, image):
    plt.imsave('./skills/%s.png' % (title), image, cmap='gray')

def save_rarity(title, image):
    plt.imsave('./rarity/%s.png' % (title), image)

def save_value(title, image):
    plt.imsave('./value/%s.png' % (title), image, cmap='gray')
