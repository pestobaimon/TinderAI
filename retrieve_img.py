import pandas as pd
import urllib.request
from urllib.parse import urlparse
import os
import progressbar

def download_img(swipe: str):
    df = pd.read_json('res/yea_gurls.json')
    df['merged'] = df.apply(lambda row: {'age':row['age'], 'img_url': row['img_url']}, axis=1)
    data = df['merged'].to_list()

    bar = progressbar.ProgressBar(maxval=len(data), \
        widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()

    for i, person in enumerate(data, start = 1):
        age = person['age']
        age = str(age)
        for url in person['img_url']:
            file_name = os.path.basename(url)
            file_name = 'age_' + age + '_' + file_name
            # print(file_name)  # Output: 09-09-201315-47-571378756077.jpg
            # download the image
            if swipe == 'left':
                try:
                    urllib.request.urlretrieve(url, "dataset/nope/" + file_name)
                except Exception:
                    pass
            else:
                try:
                    urllib.request.urlretrieve(url, "dataset/yea/" + file_name)
                except Exception:
                    pass
        bar.update(i)
    bar.finish()

download_img('right')