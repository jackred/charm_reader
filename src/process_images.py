from skimage.transform import resize
from skimage.color import rgb2gray


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


def process_image(image):
    image = image[:, :, ::-1]
    image = resize(image, shape)
    return image
