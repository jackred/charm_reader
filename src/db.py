def save_db(userID, vidID, charms, db, upsert=True):
    print(userID, vidID, db)
    db['charm_reading'].update_one(
        {'userID': userID, "videos.id": vidID},
        {'$set': {'videos.$.reading': charms, 'videos.$.done': True}}, upsert=upsert)
    

def find_one_not_done(db):
    return db['charm_reading'].find_one({"videos.done": False})
