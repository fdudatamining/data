import os
import hashlib
import pandas as pd

def int_(s):
  try:
    return int(s)
  except:
    return float('nan')

def float_(s):
  try:
    return float(s)
  except:
    return float('nan')

def money(m):
  # Remove dollar sign and commas
  return float(m[1:].replace(',',''))

def read_csv_cached(url, *kargs, **kwargs):
  cache_dir = os.environ.get('CACHE', '.cache')
  if not os.path.exists(cache_dir):
    os.mkdir(cache_dir)
  hashed_url = os.path.join(cache_dir, hashlib.md5(url.encode()).hexdigest()+'.csv')
  try:
    df = pd.read_csv(hashed_url)
  except:
    print('Downloading from %s (%s)...' % (url, hashed_url))
    df = pd.read_csv(url, *kargs, **kwargs)
    df.to_csv(hashed_url, index=False)
  return df
