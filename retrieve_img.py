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
        with open(DESTINATION, "w") as json_file:
            json.dump(json_file, list())
    
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
            json.dump(list(), to)
    if not os.path.isfile("res/archieved_nope_gurls.json"):
        with open("res/archieved_nope_gurls.json", "w") as to:
            json.dump(list(), to)

    try:
        with open('res/archieved_yea_gurls.json') as f:
            arc_yea_data = json.load(f)
    except:
        arc_yea_data = list()
    try:
        with open('res/archieved_nope_gurls.json') as f:
            arc_nope_data = json.load(f)
    except:
        arc_nope_data = list()

    with open("res/yea_gurls.json", "r") as f:
        to_insert = json.load(f)
        arc_yea_data.extend(to_insert)
    with open("res/archieved_yea_gurls.json", "w") as to:
        json.dump(arc_yea_data, to)

    with open("res/nope_gurls.json", "r") as f:
        to_insert = json.load(f)
        arc_nope_data.extend(to_insert)
    with open("res/archieved_nope_gurls.json", "w") as to:
        json.dump(arc_nope_data, to)

    print('move to archieve successfully')

def clear_json(swipe: str):

    file = 'nope_gurls.json' if swipe == 'left' else 'yea_gurls.json'

    with open(f"res/{file}", "w") as f:
            json.dump(list(), f)
            
    print(f'clear {file} successfully')

download_img('right')
download_img('left')
move_to_archieved()
clear_json('right')
clear_json('left')