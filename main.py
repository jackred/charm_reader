import numpy as np
import matplotlib.pyplot as plt
import cv2
from skimage.color import rgb2gray


ret, frame = cap.read()
plt.imshow(frame)
plt.show()

x_range = range(750, 990)
y_range = range(190, 375)

rarity_x = range(180, 239)
rarity_y = range(3, 22)

slot_x = range(150, 239)
slot_y = range(23, 47)

def get_sub_frame(frame, x, y):
    return frame[y][:, x]

def get_xrarity(frame):
    return get_sub_frame(frame, rarity_x, rarity_y)

def get_slot(frame):
    return get_sub_frame(frame, slot_x, slot_y)

def get_charm_sub_frame(frame):
    return get_sub_frame(frame, x_range, y_range)


def is_different(f1, f2):
    return ((f1 == f2).sum()/f1.size) < 0.80


def extract_frames(video):
    not_stop, frame = video.read()
    res = []
    if not_stop:
        res.append(get_charm_sub_frame(frame))
        while(not_stop):
            not_stop, frame = video.read()
            if not_stop:
                tmp = get_charm_sub_frame(frame)
                if is_different(res[-1], tmp):
                    res.append(tmp)
    return res
                

def show(f, cmap=None):
    plt.imshow(f, cmap=cmap)
    plt.show(block=False)
