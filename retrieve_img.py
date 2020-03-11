import pandas as pd
import urllib.request
from urllib.parse import urlparse
import os

df = pd.read_json('gurls.json')
df['merged'] = df.apply(lambda row: {'age':row['age'], 'name':row['name'], 'img_url': row['img_url'], 'swipe':row['swipe']}, axis=1)
data = df['merged'].to_list()

for person in data:
    age = person['age']
    age = str(age)
    swipe = person['swipe']
    for url in person['img_url']:
        file_name = os.path.basename(url)
        file_name = 'age_' + age + '_' + file_name
        print(file_name)  # Output: 09-09-201315-47-571378756077.jpg
        # download the image
        if(swipe == "left"):
            try:
                urllib.request.urlretrieve(
                    url, "dataset/nope/" + file_name)
            except Exception:
                print('save gurl failed')
        else:
            try:
                urllib.request.urlretrieve(url, "dataset/yea/" + file_name)
            except Exception:
                print('save gurl failed')