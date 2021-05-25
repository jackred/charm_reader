import numpy as np
import pandas as pd
from .utility import calculate_distance, th_slot, th_skill, th_value, \
    th_rarity, index
from .process_images import process_image, get_charm_sub_frame, get_all_infos


def find_proba(element, list_name):
    return np.array([calculate_distance(element, e)
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


def look_at_one_frame(frame, data):
    frame = process_image(frame)
    tmp = get_charm_sub_frame(frame)
    infos = get_all_infos(tmp)
    reading = read_infos_charm(infos, data)
    return reading
