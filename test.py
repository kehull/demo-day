import json
f = open('Resources\models_kelly\encoding_keys\offers_encoded.json')
data = json.load(f)

for i in data:
    print (i)