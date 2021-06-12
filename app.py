import time

from src.videos import read_video
from src.db import save_db, find_one_not_done
from src.load import load_data

from pymongo import MongoClient
from config import DBConfig

import traceback

client = MongoClient(DBConfig.host, DBConfig.port)
db = client[DBConfig.db]

FOLDER = './videos'

def save(userID, vidID, data, folder=FOLDER):
    name = "{}_{}.mp4".format(userID, vidID)
    try:
        res = read_video(folder+'/'+name, data)
        save_db(userID, vidID, res.to_dict(orient='records'), db)
    except Exception as e:
        print(e)
        traceback.print_tb(e.__traceback__)
        print('Error reading/saving files')

def main(data):
    while True:
        doc = find_one_not_done(db)
        if doc is not None:
            videos = [x for x in doc['videos'] if not x['done']]
            if len(videos) > 0:
                save(doc['userID'], videos[0]['id'], data)
                time.sleep(10)
            else:
                time.sleep(300)

if __name__ == '__main__':
    data = load_data()
    main(data)
