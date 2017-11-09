from . import *
import pandas as pd
import numpy as np

resource = 'https://data.medicare.gov/api/views/mj5m-pzi6/rows.csv?accessType=DOWNLOAD'

renames = {
  'Committed to heart health through the Million Hearts® initiative.': 'Million Hearts',
}

converters = {
  'NPI': int_,
  'PAC ID': int_,
  'Professional Enrollment ID': str,
	'Graduation year': int_,
  'Group Practice PAC ID': int_,
	'Number of Group Practice members': int_,
  'Hospital affiliation CCN 1': int_,
  'Hospital affiliation CCN 2': int_,
  'Hospital affiliation CCN 3': int_,
  'Hospital affiliation CCN 4': int_,
  'Hospital affiliation CCN 5': int_,
}

def create(con):
  print('Downloading from %s...' % (resource))
  df = read_csv_cached(resource, converters=converters)
  df = df.rename(columns=renames)

  print('Generating practitions.ccn...')
  ccn = pd.DataFrame(np.concatenate([
    df[[
      'Hospital affiliation CCN 1',
      'Hospital affiliation LBN 1',
    ]].values,
    df[[
      'Hospital affiliation CCN 2',
      'Hospital affiliation LBN 2',
    ]].values,
    df[[
      'Hospital affiliation CCN 3',
      'Hospital affiliation LBN 3',
    ]].values,
    df[[
      'Hospital affiliation CCN 4',
      'Hospital affiliation LBN 4',
    ]].values,
    df[[
      'Hospital affiliation CCN 5',
      'Hospital affiliation LBN 5',
    ]].values,
  ]), columns=[
    'Hospital affiliation CCN',
    'Hospital Affiliation LBN'
  ]).dropna().drop_duplicates()
  ccn['Hospital affiliation CCN'] = ccn['Hospital affiliation CCN'].astype(int)
  ccn.to_sql('practitioners.ccn', con, index=False, if_exists='replace')

  print('Generating practitions.primary...')
  df.drop([
    'Hospital affiliation LBN 1',
    'Hospital affiliation LBN 2',
    'Hospital affiliation LBN 3',
    'Hospital affiliation LBN 4',
    'Hospital affiliation LBN 5',
  ], axis=1).to_sql('practitioners.primary', con, index=False, if_exists='replace')
