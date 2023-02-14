import pandas as pd
from google.colab import drive
from sklearn.model_selection import train_test_split
from scipy import sparse
from scipy.sparse import csr_matrix
from tqdm.notebook import tqdm
import numpy as np
from datetime import datetime


import data
class Tunning:
  def __init__(self):
    pass
  
  def random_search(self,params, n_iters=10):
      results =[]
      for _ in tqdm(range(n_iters)):
        factor = np.random.choice(params['factor'])
        alpha = np.random.choice(params['alpha'])
        regularization = np.random.choice(params['regularization'])
        iteration = np.random.choice(params['iteration'])

        ALS = implicit.als.AlternatingLeastSquares(factors=factor, alpha=alpha, regularization=regularization, iterations=iteration,
                  random_state=42, calculate_training_loss=True)

        als = ALS_library(ALS)
        als.fit()
        hit_rate, mean_precision = als.mean_precisin_hit(5000)

        
        result = [factor, alpha, regularization, iteration, hit_rate, mean_precision]
        results.append(result)
      frame = pd.DataFrame(results, columns=['factor','alpha','regularization','iteration','hit_rate','mean_precision'])
      frame = frame.sort_values('hit_rate', ascending=False)

      return frame
  
  def grid_search(self, params):
    results =[]
    for factor in tqdm(params['factor']):
      for alpha in params['alpha']:
        for regularization in params['regularization']:
          ALS = implicit.als.AlternatingLeastSquares(factors=factor, alpha=alpha, regularization=regularization, iterations=20,
                random_state=42, calculate_training_loss=True)
          als = ALS_library(ALS)
          als.fit()
          hit_rate, mean_precision = als.mean_precisin_hit(5000)

          
          result = [factor, alpha, regularization, iteration, hit_rate, mean_precision]
          results.append(result)
        frame = pd.DataFrame(results, columns=['factor','alpha','regularization','iteration','hit_rate','mean_precision'])
        frame = frame.sort_values('hit_rate', ascending=False)
    
    return frame