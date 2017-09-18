from . import *
import pandas as pd

resources = {
  # '2009': ,
  # '2010': ,
  # '2011': ,
  # '2012': ,
  # '2013': ,
  '2014': 'https://health.data.ny.gov/api/views/rmwa-zns4/rows.csv?accessType=DOWNLOAD',
}

converters = {
  'Operating Certificate Number': int_,
  'Facility ID': int_,
  'Zip Code - 3 digits': str,
  'Length of Stay': int_,
  'Discharge Year': int_,
  'CCS Diagnosis Code': int_,
  'CCS Procedure Code': int_,
  'APR DRG Code': int_,
  'APR MDC Code': int_,
  'APR Severity of Illness Code': int_,
  'Attending Provider License Number': int_,
  'Operating Provider License Number': int_,
  'Other Provider License': int_,
  'Birth Weight': float_,
  'Total Charges': money,
  'Total Costs': money,
}

def create(con):
  df = pd.DataFrame()
  for year, resource in resources.items():
    print('Downloading year %s from %s...' % (year, resource))
    df_year = pd.read_csv(resource, converters=converters)
    df_year['Year'] = int(year)
    df = pd.concat([df, df_year])

  print('Generating diagnosis.facility...')
  df[[
    'Facility ID',
    'Facility Name'
  ]].drop_duplicates().to_sql('diagnosis.facility', con, index=False)

  print('Generating diagnosis.ccs_diagnosis...')
  df[[
    'CCS Diagnosis Code',
    'CCS Diagnosis Description'
  ]].drop_duplicates().to_sql('diagnosis.ccs_diagnosis', con, index=False)

  print('Generating diagnosis.ccs_procedure...')
  df[[
    'CCS Procedure Code',
    'CCS Procedure Description'
  ]].drop_duplicates().to_sql('diagnosis.ccs_procedure', con, index=False)

  print('Generating diagnosis.arp_drg...')
  df[[
    'APR DRG Code',
    'APR DRG Description'
  ]].drop_duplicates().to_sql('diagnosis.arp_drg', con, index=False)

  print('Generating diagnosis.arp_mdc...')
  df[[
    'APR MDC Code',
    'APR MDC Description'
  ]].drop_duplicates().to_sql('diagnosis.arp_mdc', con, index=False)

  print('Generating diagnosis.arp_severity_of_illness...')
  df[[
    'APR Severity of Illness Code',
    'APR Severity of Illness Description'
  ]].drop_duplicates().to_sql('diagnosis.arp_severity_of_illness', con, index=False)

  print('Generating diagnosis.primary...')
  df.drop([
    'Facility Name',
    'CCS Diagnosis Description',
    'CCS Procedure Description',
    'APR DRG Description',
    'APR MDC Description',
    'APR Severity of Illness Description',
  ], axis=1).to_sql('diagnosis.primary', con, index=False)
