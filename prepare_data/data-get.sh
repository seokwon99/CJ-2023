cd ..
mkdir data
cd data

mkdir korean
cd korean
wget -O ko_address.zip "https://business.juso.go.kr/addrlink/download.do?reqType=ALLRNADR_KOR&regYmd=2023&ctprvnCd=00&stdde=202306&fileName=202306_%EB%8F%84%EB%A1%9C%EB%AA%85%EC%A3%BC%EC%86%8C%20%ED%95%9C%EA%B8%80_%EC%A0%84%EC%B2%B4%EB%B6%84.zip&intNum=undefined&intFileNo=undefined&realFileName=RNADDR_KOR_2306.zip"
unzip ko_address.zip
rm ko_address.zip
cd ..

mkdir english
cd english
wget -O en_address.zip "https://business.juso.go.kr/addrlink/download.do?reqType=ALLRNADR_ENG&regYmd=2023&ctprvnCd=00&stdde=202306&fileName=202306_%EB%8F%84%EB%A1%9C%EB%AA%85%EC%A3%BC%EC%86%8C%20%EC%98%81%EC%96%B4_%EC%A0%84%EC%B2%B4%EB%B6%84.zip&intNum=undefined&intFileNo=undefined&realFileName=RN_ENG_2306.zip"
unzip en_address.zip
rm en_address.zip
cd ../..

python kor_processor.py & python en_processor.py
python combine.py