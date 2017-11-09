from . import *
import pandas as pd

resource = 'https://data.medicare.gov/api/views/ypbt-wvdk/rows.csv?accessType=DOWNLOAD'

abbreviations = {
    'Clinical Care': 'CC',
    'Process Domain Score': 'PDS',
    'Outcomes Domain Score': 'ODS',
    'Patient and Caregiver Centered Experience of Care/Care Coordination': 'PCCEC/CC',
    'Safety Domain Score': 'SDS',
    'Efficiency and Cost Reduction Domain Score': 'ECRDS',
    'Normalized': 'Norm',
}

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
  df = read_csv_cached(resource, converters=converters)

  print('Shortening column names...')
  renames = {}
  for column in df.columns:
    renamed_column = column
    for full, abbrev in abbreviations.items():
      renamed_column = renamed_column.replace(full, abbrev)
    renames[column] = renamed_column
  df = df.rename(columns=renames)

  print('Generating hospitals.meta...')
  df[[
    renames['Provider Number'],
    renames['Hospital Name'],
    renames['Address'],
    renames['City'],
    renames['State'],
    renames['ZIP Code'],
    renames['County Name'],
    renames['Location'],
  ]].to_sql('hospitals.meta', con, index=False, if_exists='replace')

  print('Generating hospitals.score...')
  df[[
    renames['Provider Number'],
    renames['Unweighted Normalized Clinical Care - Process Domain Score'],
    renames['Weighted Clinical Care - Process Domain Score'],
    renames['Unweighted Normalized Clinical Care - Outcomes Domain Score'],
    renames['Weighted Normalized Clinical Care - Outcomes Domain Score'],
    renames['Unweighted Patient and Caregiver Centered Experience of Care/Care Coordination Domain Score'],
    renames['Weighted Patient and Caregiver Centered Experience of Care/Care Coordination Domain Score'],
    renames['Unweighted Normalized Safety Domain Score'],
    renames['Weighted Safety Domain Score'],
    renames['Unweighted Normalized Efficiency and Cost Reduction Domain Score'],
    renames['Weighted Efficiency and Cost Reduction Domain Score'],
    renames['Total Performance Score'],
  ]].to_sql('hospitals.score', con, index=False, if_exists='replace')

