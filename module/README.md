
## 모듈화
- **data.py** : 데이터 전처리 및 모델에 필요한 데이터 만들기
- **Nobuy_recommend.py** : 구매하지 않은 고객을 위한 추천시스템
- **CB.py** : 구매 20건 미만인 고객에게 TF-idf를 이용한 컨텐츠 기반 추천시스템
- **ALS_implicit.py** : 구매 20건 이상인 고객에게 implicit 라이브러리를 이용한 추천시스템
- **Tunnin.py** : 최적의 하이퍼파라미터를 구하기 위한 Grid_search, Random_search 구현
