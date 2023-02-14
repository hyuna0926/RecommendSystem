from implicit.als import AlternatingLeastSquares as ALS
import implicit

import random
import os
import pandas as pd
from google.colab import drive
from sklearn.model_selection import train_test_split
from scipy import sparse
from scipy.sparse import csr_matrix
from tqdm.notebook import tqdm
import numpy as np
from datetime import datetime


class ALS_library:
  '''
  implicit 라이브러리를 이용한 ALS 모델
  '''

  def __init__(self,model):
    self.model=model
  
  def als_data(self):
    data = Data()
    train, test, upper, lower = data.customer_data()
    
    # csr matrix 만들기
    csr_train = sparse.csr_matrix((train['values'],(train['c_idx'], train['p_idx'])))
    csr_test = sparse.csr_matrix((test['values'],(test['c_idx'], test['p_idx'])))

    # 검증셋 만들기
    test_df = test.groupby('c_idx')['p_idx'].unique().to_frame().reset_index()

    #중복값 제거
    product_c = product.drop_duplicates(subset=['productDisplayName'], keep='first',ignore_index=True)
    
    return csr_train, csr_test, test_df, product_c  # 0,1,2,3


  def fit(self):
    # als 학습
    self.model.fit(self.als_data()[0])


  def recommendation(self, c_idx, k=25):
    # 추천하기  
    csr_train, csr_test, test_df, product_c = self.als_data()
    item = self.model.recommend(c_idx, csr_train[c_idx], k)[0]
    recommend = product_c[product_c['p_idx'].isin(item)]

    return recommend
  

  def mean_precisin_hit(self, user,k=25):
    csr_train, csr_test, test_df, product_c = self.als_data()

    hit = 0
    precision = 0
    users = 0
    for c_idx in range(user):
      if c_idx in test_df['c_idx'].values:
        hit_count = 0  # for문 돌 때마다 리셋
        users += 1
        recommend = self.model.recommend(c_idx, csr_train[c_idx],k)[0]
        buy_test = test_df[test_df['c_idx']==c_idx].p_idx.values[0]

        for i in buy_test:
          for j in recommend:
            if i==j:
              hit_count+=1
              precision+=1

        if hit_count >= 1: # count가 1 이상이면 hit한 것이니까 전체에 1 추가
          hit+=1

    hit_rate = hit/users
    mean_precision = (precision/25)/users

    return hit_rate, mean_precision
