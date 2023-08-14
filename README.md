### 1. data 다운로드 및 전처리 (출처: [공개하는주소](https://business.juso.go.kr/addrlink/adresInfoProvd/guidance/othbcAdresInfo.do))
```
sh prepare_data/data-get.sh
```
### 2. synthetic data 생성
```
# dataset configuration
INPUT="path/to/input.json"
OUTPUT="path/to/output.csv"
SIZE=100000
MIN=0
MAX=3

# run
python synthetic_generator.py \
    --input $INPUT \
    --output $INPUT \
    --size $SIZE \
    --min_repeat $MIN \
    --max_repeat $MAX
```

### 3. Available Data for Download
   
| data      | count | type | path |
|  -----  | ----- | ---- | ---- |
| train | 400k | 1+2 | [train_final.csv](https://drive.google.com/file/d/10Ofba0fTu8kjxa2X6oLqEO1CAtU7JlNc/view?usp=drive_link) |
| ┗ train-papago | 150k | 1 | [train_papago_0714.csv](https://drive.google.com/file/d/1ckDWZrksa2E1ixT2jbxu1HxGQjBo8y7x/view?usp=drive_link) |
| ┗ train-synthetic | 250k |   2  | ---- |
|  dev-synthetic  | 50k | 2 | [dev_final.csv](https://drive.google.com/file/d/1oURLfPk6UYG4JhuRlfHCwkEZ-yukAawx/view?usp=drive_link) |
