import json

try:
    with open('gurls.json') as f:
        data = json.load(f)
except:
    data = list()
print(data)
data.append({
            'age': 'testage',
            'name': 'testname',
            'img_url': 'test'
            })
with open('gurls.json', 'w') as json_file:
    json.dump(data, json_file)

# print(type(data))
