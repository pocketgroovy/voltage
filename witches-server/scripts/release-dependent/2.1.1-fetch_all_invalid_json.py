
import sys
import json
import StringIO
import zipfile


from pymongo import MongoClient

# this retrieves all JSONs that don't have an available scene and at least one completed scene
def main(argv):

    db = MongoClient("mongodb://localhost:27017")
    # db = MongoClient("mongodb://10.114.239.69:27017")     # production


    print "starting invalid json fetch..."
    
    userplayerjson_collection = db.witches.UserPlayerJson
    wuser_collection = db.witches.WUsers

    docs = userplayerjson_collection.find()

    zip_buffer = StringIO.StringIO()
    zip_archive = zipfile.ZipFile(zip_buffer, mode='w')


    iOS_id_list = []
    iOS_json_list = []

    android_id_list = []
    android_json_list = []

    unknown_id_list = []
    unknown_json_list = []

    for doc in docs:
        playerjson = json.loads(doc['playerjson'])

        if not playerjson['availableScenes'] and playerjson['completedScenes']:
            phone_id = doc['phone_id']

            wuser = wuser_collection.find_one({"phone_id": phone_id})
            device = wuser['device']

            # switch = {
            #     'Android': (lambda: android_id_list, android_json_list),
            #     'IPhonePlayer': (lambda: iOS_id_list, iOS_json_list)
            # }

            # id_list, json_list = switch.get(device, (lambda: unknown_id_list, unknown_json_list))
            # id_list.append(phone_id)
            # json_list.append(json.dumps(playerjson, indent=4, separators=(',', ': ')))

            playerjson['SUPPORT'] = {}
            playerjson['SUPPORT']['MONGO_ID'] = str(wuser['_id'])
            playerjson['SUPPORT']['DEVICE'] = wuser['device']

            if device == 'Android':
                android_id_list.append(phone_id)
                android_json_list.append(json.dumps(playerjson, indent=4, separators=(',', ': ')))
            elif device == 'IPhonePlayer':
                iOS_id_list.append(phone_id)
                iOS_json_list.append(json.dumps(playerjson, indent=4, separators=(',', ': ')))
            else:
                unknown_id_list.append(phone_id)
                unknown_json_list.append(json.dumps(playerjson, indent=4, separators=(',', ': ')))


    device_package("Android", android_id_list, android_json_list, zip_archive)
    device_package("iOS", iOS_id_list, iOS_json_list, zip_archive)
    device_package("Unknown", unknown_id_list, unknown_json_list, zip_archive)

    zip_archive.close()

    print zip_archive.printdir()    
    total_invalid = len(iOS_id_list) + len(android_id_list) + len(unknown_id_list)
    print "ios: {0}\tandroid: {1}\tunknown: {2}\ttotal: {3} [of {4} docs]".format(  len(iOS_id_list), 
                                                                                    len(android_id_list),
                                                                                    len(unknown_id_list),
                                                                                    total_invalid,
                                                                                    docs.count())

    # maybe should prefix with date
    with open('no_available_scene_json.zip', 'w') as f:
        f.write(zip_buffer.getvalue())

    db.close()


def device_package(path, id_list, json_list, archive):
    archive.writestr("{0}/id_manifest.json".format(path), json.dumps(id_list, indent=4, separators=(',', ': ')))
    for index,player_id in enumerate(id_list):
        archive.writestr("{0}/{1}.json".format(path, player_id), json_list[index])

    return archive

if __name__ == '__main__':
    main(sys.argv)








# db = MongoClient("mongodb://localhost:27017")
# userplayerjson_collection = db.witches.UserPlayerJson

# docs = userplayerjson_collection.find()
# # print "total documents: " + str(docs.count())

# # for doc in docs:

# zip_buffer = StringIO.StringIO()
# zip_archive = zipfile.ZipFile(zip_buffer, mode='w')


# id_list = []
# json_list = []
# for doc in docs:
#     playerjson = json.loads(doc['playerjson'])

#     if not playerjson['availableScenes']:
#         id_list.append(doc['phone_id'])
#         json_list.append(json.dumps(playerjson, indent=4, separators=(',', ': ')))


# zip_archive.writestr('id_manifest.txt', json.dumps(id_list, indent=4, separators=(',', ': ')))
# for index,player_id in enumerate(id_list):
#     zip_archive.writestr(player_id + '.json', json_list[index])

# zip_archive.close()
# print zip_archive.printdir()    
# print "invalid json count: {0} [of {1} docs]".format(len(id_list), docs.count())

# with open('no_available_scene_json.zip', 'w') as f:
#     f.write(zip_buffer.getvalue())

# db.close()







# json_file = StringIO.StringIO()
# json_file.write(json.dumps(doc['playerjson']))
# files.append(StringIO.String())
# files[i].getvalue()