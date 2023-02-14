class Data:
  '''
  c_idx를 입력했을 때 원하는 데이터 나올 수 있게 하기!
  1. 아예 없는 경우
  2. 구매하지 않은 회원(customer_info.parquet)
  3. 20개 미만 산 회원(cart_purchase)
  4. 20개 이상 산 회원(cart_purchase)
  '''
  def __init__(self):
    pass


  def customer_info(self, c_idx):
    # 비회원
    if c_idx not in customer_info['c_idx']:
      print(c_idx, '님은 회원정보가 없습니다.')

    # 구매하지 않는 회원
    elif c_idx not in cart_purchase['c_idx']:
      print(c_idx, '님은 구매이력이 없습니다.')

    # 20개 이상 산 회원
    elif c_idx in self.customer_data()[2]['c_idx'].values: # upper
      print(c_idx, '님은 20개 이상 구매한 회원입니다. ALS 진행')
      
    elif c_idx in self.customer_data()[3]['c_idx'].values: #lower
      print(c_idx, '님은 20개 미만 구매한 회원입니다. CB 진행')

    return c_idx

  
  def customer_data(self):
    '''
    ALS와 CB 데이터 만들기

    return 
    train, test : ALS
    upper, lower : CB(20개 기준으로 나눔)
    '''
    df = cart_purchase.copy()
    df['values'] = 1  # 구매, 장바구니니까 1로 implicit 데이터

    df_group = df.groupby(['c_idx'], as_index=False).count()


    # ALS(20개 이상)
    upper = df[df['c_idx'].isin(df_group.query('values>=20').c_idx)] # 20개 이상
    test = upper.groupby('c_idx').sample(frac=0.2, random_state=42) # als_test
    train = upper.drop(test.index) # als_train
    
    # CB(20개 미만)
    lower = df[df['c_idx'].isin(df_group.query('values<20').c_idx)] # 20개 미만

    return train, test, upper, lower
  


  def no_purchase_data(self):
    '''
    회원정보는 있지만 구매하지 않은 사람을 위한 나이별 데이터 만들기
    customer_info와 cart_purchase 합치기

    return
    youth : 20대 이하 구매 이력
    age_20 : 20대 구매 이력
    age_30 : 30대 이상 구매 이력
    '''
    customer_c = customer_info.copy()
    customer_c.birthdate = customer_c.birthdate.apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))
    customer_c['age']=customer_c.birthdate.apply(lambda x: datetime.today().year - x.year)

    cus_pur = pd.merge(cart_purchase, customer_c, on=['c_idx','customer_id'], how='left')
    customer_nobuy = customer_c[~customer_c['c_idx'].isin(cus_pur['c_idx'])]

    #데이터 분리
    youth = cus_pur.query("age<20")  # 20대 이하 구매 이력
    age_20 = cus_pur.query('age>=20 and age<30')  # 20대 구매 이력
    age_30 = cus_pur.query('age>=30')  # 30대 이상 구매 이력

    youth_nobuy = customer_nobuy.query("age<20")  # 20대 이하 구매 이력
    age_20_nobuy = customer_nobuy.query('age>=20 and age<30')  # 20대 구매 이력
    age_30_nobuy = customer_nobuy.query('age>=30')  # 30대 이상 구매 이력

    return youth, age_20, age_30 , youth_nobuy, age_20_nobuy, age_30_nobuy