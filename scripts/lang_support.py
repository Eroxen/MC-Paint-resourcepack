import json
import os
import glob

path = '../assets/minecraft/lang'

with open(os.path.join(path, 'en_us.json'), 'r') as file:
    all_keys = set(json.load(file).keys())

for filepath in glob.glob(os.path.join(path, '*.json')):
    lang = os.path.splitext(os.path.split(filepath)[1])[0]
    print(lang)
    with open(filepath, 'r') as file:
        keys = {k for k in set(json.load(file).keys()) if k in all_keys}
    print(f"{lang}: {100*len(keys)/len(all_keys)}%")

# print(all_keys)