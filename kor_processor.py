import os
import json
from tqdm import tqdm

data_dir = './data/korean'
combined_korean = './processed/preprocessed_korean.json'

doromyung = [
    "도로명주소관리번호",
    "법정동코드",
    "시도명",
    "시군구명",
    "읍면동명",
    "리명",
    "산여부",
    "번지",
    "호",
    "도로명코드",
    "도로명",
    "지하여부",
    "건물본번",
    "건물부번",
    "행정동코드",
    "행정동명",
    "기초구역번호(우편번호)",
    "이전도로명주소",
    "효력발생일",
    "공동주택구분",
    "이동사유코드",
    "건축물대장건물명",
    "시군구용건물명",
    "비고"
]

zibun = [
    "도로명주소관리번호",
    "법정동코드",
    "시도명",
    "시군구명",
    "법정읍면동명",
    "법정리명",
    "산여부",
    "지번본번(번지)",
    "지번부번(호)",
    "도로명코드",
    "지하여부",
    "건물본번",
    "건물부번",
    "이동사유코드"
]

raw_korean = {}
for name in os.listdir(data_dir):
    if 'txt' not in name:
        continue
    print(name)
    data_path = os.path.join(data_dir, name)
    with open(data_path, 'r', encoding='cp949') as f:
        raw_korean[data_path] = f.readlines()

combined = {}
combined['zibun'] = []
combined['doromyung'] = []
for key in tqdm(raw_korean):
    data = raw_korean[key]
    for d in data:
        parsed = d.split('|')
        new_d = dict()
        ## 지번
        if len(parsed) == 14:
            for c, p in zip(zibun, parsed):
                new_d[c] = p
            combined['zibun'].append(new_d)
        ## 도로명주소
        else:
            for c, p in zip(doromyung, parsed):
                new_d[c] = p
            combined['doromyung'].append(new_d)

with open(combined_korean, 'w') as f:
    json.dump(combined, f, indent=4, ensure_ascii=False)