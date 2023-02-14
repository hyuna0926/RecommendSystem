# RecommendSystem
## 프로젝트 개요
![image](https://user-images.githubusercontent.com/110091343/218765593-66d06397-6cae-41a3-88b4-2283af9fae1d.png)

코로나19 대유행으로 비대면 문화가 확산되고 디지털 전환이 가속화됨에 따라 이커머스 시장은 급격한 성장을 이루었습니다. 하지만 2017년 이후 연평균 20%대의 고성장을 기록하던 이커머스 시장이 저성장 구간에 진입하는 것으로 보입니다. 증권가는 올해 국내 온라인 쇼핑 시장의 [성장률이 9~13% 수준](https://biz.chosun.com/distribution/channel/2022/01/10/VURET6JTVZARXN7HQ4W6TYW6AY/)으로 하락할 것으로 전망합니다.

따라서 이런 시대에서 살아남기 위해 우리는 이커머스 고객 행동 데이터를 기반으로 추천시스템을 구축해 매출을 상승을 목표로 하고 있습니다.

## 데이터 정보

- transaction_new.csv
- customer.csv
- product.csv
- click_stream_new.csv

출처 : [https://www.kaggle.com/datasets/latifahhukma/fashion-campus](https://www.kaggle.com/datasets/latifahhukma/fashion-campus)

## 프로젝트 과정
![image](https://user-images.githubusercontent.com/110091343/218764575-39043c92-c5c2-4c2e-8811-b0d9b0685675.png)


1. **데이터 경량화**
    - OOM(Out Of Memory) 문제 발생
    - object → category / int64 → int32  변경
    - csv → parquet 저장
2. **데이터 전처리**
    - click_stream_new에서 add_to_cart만 뽑아 transaction_new 데이터와 합쳐줌
        - cart_purchase.parquet
        - 데이터 1876781개
        - c_idx 50689개
        - p_idx 31121개
        - implicit 데이터이기 때문에 1을 넣은 새로운 컬럼을 만들어줌
    - csr_matrix에서 0인 값이 약 99.9048%
    - customer, product 데이터
3. **데이터 분석**
    - 고객 세분화
        - 전환이 일어난 고객 중 20개 이상 구매한 고객에게 implicit 라이브러리를 사용
        - 20개 미만으로 구매한 고객에게는 TF-idf를 이용한 컨텐츠 기반 추천을 진행
        - 전환이 일어나지 않은 고객 중 고객 정보가 있는 사람에게는 연령 별 인기 많은 상품을 추천
        - 정보가 없는 고객은 제일 많이 팔린 상품을 추천
4. **추천시스템** 
    - implicit 라이브러리 이용해 추천시스템 구축
    - TF-idf를 이용한 컨텐츠 기반 추천시스템 구축
5. **추천시스템 성능 평가 및 개선**
    - gridsearch, randomsearch로 성능 개선

## 데이터 분석 및 결과

### **고객 세분화 및 추천모델**
![image](https://user-images.githubusercontent.com/110091343/218764503-4b5ef119-fdc9-4928-8feb-f69882e765c9.png)



### **CB**
- TF-idf를 이용한 컨텐츠 기반 추천시스템
- 데이터가 많아 남녀 별로 코사인 유사도를 구함
    - 남자 ['Men','Boys','Unisex'] 17712개
    - 여자 ['Women','Girls','Unisex'] 15157개
    - Unisex는 모두 포함
- 고객이 가장 최근에 구매한 상품과 유사도가 높은 상품 추천

### **ALS**

![image](https://user-images.githubusercontent.com/110091343/218764668-01d08a4d-df4a-478e-b93b-bd6dbab04b29.png)


- 추천해주는 상품을 보면 고객이 shoes를 많이 구매했는데 추천 상품에도 shoes가 많은 것을 알 수 있음.

#### **ALS - 최적의 하이퍼파라미터를 위한 Grid, Random search 진행**

![image](https://user-images.githubusercontent.com/110091343/218764767-7e5add3d-e9d2-4276-909d-cee0403ed8aa.png)

- 베이스라인(가장 많이 팔린 25개와 비교)
    - mean_precision@k : 0.0139
    - mean_hit_rate@k : 0.2644
- 베이스라인보다 성능이 높게 나왔음

## 회고

**전현아**

- fashion campus 데이터 중 click_stream_new에서 어떤 상품을 클릭했는지 봤는지 나와있지 않았음, 그래서 상품아이디가 존재하는 add_to_cart만 사용했음. 고객의 관심상품을 자세히 알 수 없어 아쉬웠음.
- 상품 데이터가 너무 방대해 hit rate, precision@k가 많이 낮게 나왔음.
- LightFM 모델도 사용했지만 똑같은 상품을 추천해 역확률가중치를 이용했지만 똑같은 결과가 나왔음.
- 이번 기회에 추천시스템에 대해 많은 것을 알고 배울 수 있어 뿌듯함.
- 이커머스 관련 도메인지식이 부족했지만 이번에 공부하면서 제대로 공부해서 지식을 쌓을 수 있었음.

**홍영신**
- ㅇㅇㅇㅇ








## 참고자료

[pyconkr2019_뚱뚱하고 굼뜬 판다를 위한 효과적인 다이어트 전략_20190817](https://drive.google.com/file/d/12faqaslFIF-Sg_sU3jeGyauW5ClRqS8D/view)

[https://shopigate.co.kr/blogs/news/d2c-direct-to-consumer-비즈니스를-시작해야-하는-이유](https://shopigate.co.kr/blogs/news/d2c-direct-to-consumer-%EB%B9%84%EC%A6%88%EB%8B%88%EC%8A%A4%EB%A5%BC-%EC%8B%9C%EC%9E%91%ED%95%B4%EC%95%BC-%ED%95%98%EB%8A%94-%EC%9D%B4%EC%9C%A0)
