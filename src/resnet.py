from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np
import json
import os
model = ResNet50(weights='imagenet')

def create_animals_dict(path_json):
    '''
    from the official list of codes, i extract the first 397 names (all animals)
    and create a dict with codes->name
    '''
    p= json.load(open(path_json))
    animals_codes = {}
    indexes = [x for x in p.keys() if int(x)<398]
    for i in indexes:
        animals_codes[p.get(i)[0]] = p.get(i)[1]

    return animals_codes

def ResNet50_predict(img_path,anim_codes):
    '''
    the model opens the img in the path and predicts the most likely labels between the 1000 provided
    it also checks if if's an animal (based on the most likely label)
    '''
    #extracting img name
    img_name = img_path.split("/")[-1]
    #preprocessing
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    #predictions
    preds = model.predict(x)
    
    #i care about the first result
    results = decode_predictions(preds, top=3)[0][0]
    percentage = str(round(results[2]*100,2))+"%"
    print(f'\n{img_name} Predicted:', decode_predictions(preds, top=3)[0])

    #check if it's an animal
    if results[0] in anim_codes.keys():
        print("Found an animal! "+img_name+" -> "+results[1])
        return True, img_name, results[1], percentage

    else: 
        return False, img_name, results[1], percentage


def select_animal_memes(directory,path_json):
    '''
    from the results of the model i must pick the first n memes
    '''
    
    selected_memes, others = [],[]
    num_memes = os.environ.get("NUM_MEMES")
    anim_codes = create_animals_dict(path_json)

    #sorting by natural numbers: 1,2,3,12,21 not 1,11,12,2,21
    for file in sorted(os.listdir(directory),key=len):
        if file.endswith(".jpg"):
            
            resnet_res =  ResNet50_predict(directory+file,anim_codes)
            if resnet_res[0]:
                selected_memes.append(resnet_res)
            else: others.append(resnet_res)

    if len(selected_memes) < num_memes:
        #if I don't find animals I'll complete the list with the first x "non-animal" memes
        missing = num_memes-len(selected_memes)
        selected_memes = selected_memes+others[:missing]

    return selected_memes
