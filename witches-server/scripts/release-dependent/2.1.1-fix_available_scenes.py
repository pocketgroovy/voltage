
import os
import json


# iterates through directory of jsons and replaces available scenes

SCRIPT_DIR = "./iOS_orig"
OUTPUT_DIR = "./iOS_fixed"
SCENE = "Rhys-Ty Main Story/RT Ireland/The Possibilities"


for filename in os.listdir(SCRIPT_DIR):
    
    filepath = os.path.join(SCRIPT_DIR, filename)
    # print filepath

    if filepath.endswith('.json') and filename != 'id_manifest.json':
        with open(filepath, 'r') as inputfile:
            json_obj = json.load(inputfile)

            print "processing: " + json_obj['userID']
            json_obj['availableScenes'] = [SCENE]

            if not os.path.exists(OUTPUT_DIR):
                os.makedirs(OUTPUT_DIR)

            output_path = os.path.join(OUTPUT_DIR, filename)

            with open(output_path, 'w') as outfile:
                json.dump(json_obj, outfile, indent=4, separators=(',', ': '))







