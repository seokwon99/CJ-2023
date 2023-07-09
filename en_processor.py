import os
import json
from tqdm import tqdm

data_dir = './data/english'
combined_english = './processed/preprocessed_english.json'

columns = [
    "도로명주소관리번호",
    "법정동코드",
    "영문시도명",
    "영문시군구명",
    "영문읍면동명",
    "영문리명",
    "도로명코드",
    "영문도로명",
    "지하여부",
    "건물본번",
    "건물부번",
    "기초구역번호(우편번호)",
    "산여부",
    "번지",
    "호",
    "효력발생일",
    "이동사유코드",
]

raw_english = {}
for name in os.listdir(data_dir):
    if 'txt' not in name:
        continue
    print(name)
    data_path = os.path.join(data_dir, name)
    with open(data_path, 'r', encoding='cp949') as f:
        raw_english[data_path] = f.readlines()

combined = {}
combined['doromyung'] = []
for key in tqdm(raw_english):
    data = raw_english[key]
    for d in data:
        parsed = d.split('|')
        new_d = dict()
        for c, p in zip(columns, parsed):
            new_d[c] = p
        combined['doromyung'].append(new_d)

with open(combined_english, 'w') as f:
    json.dump(combined, f, indent=4, ensure_ascii=False)