from . import *
import pandas as pd

resource = 'https://data.medicare.gov/api/views/ypbt-wvdk/rows.csv?accessType=DOWNLOAD'

converters = {
  'Provider Number': int_,
  'ZIP Code': str,
  'Unweighted Normalized Clinical Care - Process Domain Score': float_,
  'Weighted Clinical Care - Process Domain Score': float_,
  'Unweighted Normalized Clinical Care - Outcomes Domain Score': float_,
  'Weighted Normalized Clinical Care - Outcomes Domain Score': float_,
  'Unweighted Patient and Caregiver Centered Experience of Care/Care Coordination Domain Score': float_,
  'Weighted Patient and Caregiver Centered Experience of Care/Care Coordination Domain Score': float_,
  'Unweighted Normalized Safety Domain Score': float_,
  'Weighted Safety Domain Score': float_,
  'Unweighted Normalized Efficiency and Cost Reduction Domain Score': float_,
  'Weighted Efficiency and Cost Reduction Domain Score': float_,
  'Total Performance Score': float_,
}

def create(con):
  print('Downloading from %s...' % (resource))
  df = pd.read_csv(resource, converters=converters)

  print('Generating hospitals.meta...')
  df[[
    'Provider Number',
    'Hospital Name',
    'Address',
    'City',
    'State',
    'ZIP Code',
    'County Name',
    'Location',
  ]].to_sql('hospitals.meta', con, index=False)

  print('Generating hospitals.score...')
  df[[
    'Provider Number',
    'Unweighted Normalized Clinical Care - Process Domain Score',
    'Weighted Clinical Care - Process Domain Score',
    'Unweighted Normalized Clinical Care - Outcomes Domain Score',
    'Weighted Normalized Clinical Care - Outcomes Domain Score',
    'Unweighted Patient and Caregiver Centered Experience of Care/Care Coordination Domain Score',
    'Weighted Patient and Caregiver Centered Experience of Care/Care Coordination Domain Score',
    'Unweighted Normalized Safety Domain Score',
    'Weighted Safety Domain Score',
    'Unweighted Normalized Efficiency and Cost Reduction Domain Score',
    'Weighted Efficiency and Cost Reduction Domain Score',
    'Total Performance Score',
  ]].to_sql('hospitals.score', con, index=False)

