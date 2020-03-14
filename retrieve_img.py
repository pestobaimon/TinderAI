import pandas as pd
import urllib.request
from urllib.parse import urlparse
import os
import progressbar
import json

def download_img(swipe: str):
    if swipe == 'right':
        print('downloading yea img...')
    else:
        print('downloading nope img...')

    df = pd.read_json('res/yea_gurls.json')
    df['merged'] = df.apply(lambda row: {'age':row['age'], 'img_url': row['img_url']}, axis=1)
    data = df['merged'].to_list()

    bar = progressbar.ProgressBar(maxval=len(data), \
        widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()

    for i, person in enumerate(data, start = 1):
        age = person['age']
        age = str(age)
        url = person['img_url']
        file_name = os.path.basename(url)
        file_name = 'age_' + age + '_' + file_name
        if swipe == 'right':
            try:
                urllib.request.urlretrieve(url, "dataset/yea/" + file_name)
            except Exception:
                collect_failed_gurl(person, 'right')
        else:
            try:
                urllib.request.urlretrieve(url, "dataset/nope/" + file_name)
            except Exception:
                collect_failed_gurl(person, 'left')
        bar.update(i)

    bar.finish()

def collect_failed_gurl(gurl, status: str):

    DESTINATION = 'res/failed_yea_gurls.json' if status == 'right' else 'res/failed_nope_gurls.json'
    
    if not os.path.isfile(DESTINATION):
        with open(DESTINATION, "w") as to:
            pass
    
    try:
        with open(DESTINATION) as f:
            data = json.load(f)
    except:
        data = list()

    data.append(gurl)

    try:
        with open(DESTINATION, 'w') as json_file:
            json.dump(data, json_file)
    except:
        pass

def move_to_archieved():
    if not os.path.isfile("res/archieved_yea_gurls.json"):
        with open("res/archieved_yea_gurls.json", "w") as to:
            json.dump(to, list())
    if not os.path.isfile("res/archieved_nope_gurls.json"):
        with open("res/archieved_nope_gurls.json", "w") as to:
            json.dump(to, list())

    with open("res/yea_gurls.json", "r") as f, open("res/archieved_yea_gurls.json", "r") as to:
        to_insert = json.load(f)
        destination = json.load(to)
        destination.append(to_insert) #The exact nature of this line varies. See below.
    with open("res/archieved_yea_gurls.json", "w") as to:
        json.dump(to, destination)
    with open("res/nope_girls.json", "r") as f, open("res/archieved_nope_gurls.json", "r") as to:
        to_insert = json.load(f)
        destination = json.load(to)
        destination.append(to_insert) #The exact nature of this line varies. See below.
    with open("res/archieved_nope_gurls.json", "w") as to:
        json.dump(to, destination)
    print('moved to archieve successfully')

def clear_json():
    with open("res/yea_gurls.json", "w") as f:
        json.dump(f, '')
    with open("res/nope_gurls.json", "w") as f:
        json.dump(f, '')
    print('clear files successfully')

download_img('right')
download_img('left')
move_to_archieved()
clear_json()
