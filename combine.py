import json
import os

kor_data_path = "processed/preprocessed_korean.json"
en_data_path = "processed/preprocessed_english.json"

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
    
with open('combined.json', 'w') as f:
    json.dump(new_data, f, indent=4, ensure_ascii=False)