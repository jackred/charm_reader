import matplotlib.pyplot as plt
import numpy as np

th_slot = 20
th_skill = 70
th_value = 13
th_rarity = 40

threshold = {'rarity': th_rarity, 'skill_1': th_skill, 'value_1': th_value,
             'skill_2': th_skill, 'value_2': th_value, 'slot_1': th_slot,
             'slot_2': th_slot, 'slot_3': th_slot}

index = list(threshold.keys())


def show(f, cmap=None):
    plt.imshow(f, cmap=cmap)
    plt.show(block=False)


def calculate_distance(i1, i2):
    return np.sum((i1-i2)**2)


def is_different(f1, f2):
    return ((f1 == f2).sum()/f1.size) < 0.80


def same_infos(i1, i2):
    return all([calculate_distance(i1[i], i2[i]) < threshold[i]
                for i in i2])
