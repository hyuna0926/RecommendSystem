import data
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class CB_recommend():
  '''
  20개 미만 구매한 고객에게 성별 별로 추천하기
  tf-idf를 이용한 컨텐츠 기반 추천시스템
  '''
  def __init__(self):
    pass
  
  def CB_data(self):
    '''
    CB data 만들어주기
    성별 나눠줌
    - 남자 ['Men','Boys','Unisex'] 17712개
    - 여자 ['Women','Girls','Unisex'] 15157개
    - Unisex는 모두 포함

    return 
    Men : 남성 상품 정보
    Women : 여성 상품 정보
    product_c : 중복값을 제거한 전체 상품 정보
    '''

    # product 중복값 제거
    product_c = product.drop_duplicates(subset=['productDisplayName'], keep='first',ignore_index=True)
    # 결측값 제거
    df = product_c.copy()
    df.dropna(subset=['productDisplayName','year'],inplace=True)
    col = ['baseColour','season','usage']
    df[col]=df[col].astype('object')
    df[col] = df[col].fillna("unknown") #결측값 채워주기
    df[col]=df[col].astype('category')
    
    #tf-idf를 위해 컬럼 만들어주기
    df['features'] = df[['gender','articleType','baseColour','season','usage']].apply(' '.join, axis=1)

    # 성별 나눠주기
    men = ['Men','Boys','Unisex']
    women = ['Women','Girls','Unisex']
    Men = df[df['gender'].isin(men)]
    Women = df[df['gender'].isin(women)]

    return Men, Women ,product_c

  def tfidf(self):
    '''
    tf-idf을 이용한 컨텐츠 기반 추천시스템
    남녀별로 코사인 유사도 진행 
    
    return cosine_men, cosine_women
    '''
    Men, Women, product_c = self.CB_data()

    tfidf_m = TfidfVectorizer()
    tfidf_men = tfidf_m.fit_transform(Men['features'])
    tfidf_w = TfidfVectorizer()
    tfidf_women = tfidf_w.fit_transform(Women['features'])


    #코사인 유사도
    cosine_men = pd.DataFrame(cosine_similarity(tfidf_men,tfidf_men),index = Men.p_idx, columns=Men.p_idx)
    cosine_women = pd.DataFrame(cosine_similarity(tfidf_women,tfidf_women),index = Women.p_idx, columns=Women.p_idx)

    return cosine_men, cosine_women


  def recommend(self, c_idx, k=25):
    '''
    Data클래스에 있는 데이터 들고오기
    남자/여자 나눠서 추천
    최근에 산 제품과 유사한 상품 k개 추천

    return recommend(유사한 상품 k개)
    '''
    data = Data()
    lower = data.customer_data()[3] # 20개 이하 구매한 사람

    Men, Women, product_c = self.CB_data()
    cosine_men, cosine_women = self.tfidf()

    # 고객이 최근에 산 상품
    buy_recent = lower[lower['c_idx']==c_idx].sort_values(by='created_at', ascending=False)[:1]  
    p_idx = buy_recent.p_idx.values[0]


    if p_idx in Men['p_idx']: #상품 p_idx가 Men에 들어가있으면
      men_sim = cosine_men[p_idx].sort_values(ascending=False).index
      recommend = product_c[product_c['p_idx'].isin(men_sim)][:k]
    
    else: # Women에 들어가있으면
      women_sim = cosine_women[p_idx].sort_values(ascending=False).index
      recommend = product_c[product_c['p_idx'].isin(women_sim)][:k]

    return recommend
    