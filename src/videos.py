import os
import cv2
import time
import pandas as pd
from .utility import index, calculate_distance
from .load import load_data
from .read import look_at_one_frame
from .save import save_csv
from .process_images import process_image, get_charm_sub_frame


# to clean
def read_frames(video, data):
    not_stop, frame = video.read()
    res = pd.DataFrame(columns=index)
    if not_stop:
        reading = look_at_one_frame(frame, data)
        if not (reading[['skill_1', 'slot_1', 'slot_2', 'slot_3', 'rarity']]
                == '').any():
            # kinda useless to index in reading before but eh
            res = res.append(reading, ignore_index=True)
        while(not_stop):
            not_stop, frame = video.read()
            if not_stop:
                reading = look_at_one_frame(frame, data)
                if not (reading[['skill_1', 'slot_1', 'slot_2', 'slot_3',
                                 'rarity']] == '').any() \
                        and (len(res) == 0
                             or not ((reading == res.iloc[-1]).all())):
                    res = res.append(reading, ignore_index=True)
    return res


def read_video(filename, data):
    cap = cv2.VideoCapture(filename)
    res = read_frames(cap, data)
    cap.release()
    os.remove(filename)
    return res


def read_videos(folder_name):
    data = load_data()
    files = os.listdir(folder_name)
    files.sort()
    res = pd.DataFrame(columns=index)
    for i in files:
        if i[-4:] == '.mp4':
            print('Reading {}'.format(i))
            res = res.append(read_video(folder_name + '/' + i, data))
    return res


def read_videos_store_csv(folder_name):
    if 'output' not in os.listdir(folder_name):
        os.mkdir(folder_name+'/output')
    charms = read_videos(folder_name)
    save_csv(charms,
             folder_name + '/output/output_{}.csv'.format(int(time.time())))


# utility look at data
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
                if calculate_distance(tmp, fp) > 30:
                    res.append(tmp)
                    fp = tmp
    return res
