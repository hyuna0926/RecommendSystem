import pandas as pd
from google.colab import drive
from sklearn.model_selection import train_test_split
from scipy import sparse
from scipy.sparse import csr_matrix
from tqdm.notebook import tqdm
import numpy as np
from datetime import datetime

import data

class Nobuy_recommend:
  def __init__(self):
    pass
  
  def nobuy_recommend(self,c_idx, k=25):
    '''
    아무 정보 없는 사람과 구매 이력이 없는 사람에게 추천
    '''
    data = Data()
    youth, age_20, age_30, youth_nobuy, age_20_nobuy, age_30_nobuy = data.no_purchase_data()
    product_c = product.drop_duplicates(subset=['productDisplayName'], keep='first',ignore_index=True)

    if c_idx not in customer_info['c_idx'].values:  # 회원정보가 없는
      item = cart_purchase.groupby('p_idx').count()['created_at'].sort_values().tail(k).index
      recommend = product_c[product_c['p_idx'].isin(item)]
      print('회원정보가 없어 가장 많이 팔린 제품을 추천합니다')

    elif c_idx in youth_nobuy['c_idx'].values: #20세 미만
      item = youth.groupby('p_idx').count().sort_values(by='created_at').tail(k).index
      recommend= product_c[product_c['p_idx'].isin(item)]
      print('회원님! 20대 미만인 고객님들이 가장 많이 구매한 상품을 추천합니다.')
  
    elif c_idx in age_20_nobuy['c_idx'].values: #20대
      item = age_20.groupby('p_idx').count().sort_values(by='created_at').tail(k).index
      recommend= product_c[product_c['p_idx'].isin(item)]
      print('20대 회원님! 20대인 고객님들이 가장 많이 구매한 상품들을 추천합니다.')
    
    else: #30대 이상
      item = age_30_nobuy.groupby('p_idx').count().sort_values(by='created_at').tail(k).index
      recommend= product_c[product_c['p_idx'].isin(item)]
      print('30대 이상인 회원님! 30대 이상인 고객님들이 가장 많이 구매한 상품들을 추천합니다.')

    return recommend