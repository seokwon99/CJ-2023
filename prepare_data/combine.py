import json
import os
import random

kor_data_path = "../processed/preprocessed_korean.json"
en_data_path = "../processed/preprocessed_english.json"
DATA_SIZE = 1000000

with open(kor_data_path) as k, open(en_data_path) as e:
    kor = json.load(k)
    en = json.load(e)
    korean_doromyung = kor['doromyung']
    korean_zibun = kor['zibun']
    english_doromying = en['doromyung']

new_data = {}

for d in korean_doromyung:
    key = d["도로명주소관리번호"]
    if key not in new_data:
        new_data[key] = {}
    new_data[key]['k_doro'] = d

for d in korean_zibun:
    key = d["도로명주소관리번호"]
    if key not in new_data:
        new_data[key] = {}
    new_data[key]['k_zibun'] = d
    
for d in english_doromying:
    key = d["도로명주소관리번호"]
    if key not in new_data:
        new_data[key] = {}
    new_data[key]['e_doro'] = d

processed_data = {}
for key in new_data:
    if 'k_doro' not in new_data[key] or 'k_zibun' not in new_data[key] or 'e_doro' not in new_data[key]:
        continue
    processed_data[key] = new_data[key]

def dictionary_sampling(data, size):
    keys = list(data.keys())
    rand_keys = random.sample(keys, size)
    new_dict = {}
    for key in rand_keys:
        new_dict[key] = data[key]
    return new_dict

processed_data = dictionary_sampling(processed_data, DATA_SIZE)

with open('../processed/combined.json', 'w') as f:
    json.dump(processed_data, f, indent=4, ensure_ascii=False)