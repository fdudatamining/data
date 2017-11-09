from . import *
import pandas as pd

# https://health.data.ny.gov/en/browse?q=Hospital+Inpatient+Discharges+%28SPARCS+De-Identified%29
resources = {
  '2009': 'https://health.data.ny.gov/api/views/q6hk-esrj/rows.csv?accessType=DOWNLOAD',
  '2010': 'https://health.data.ny.gov/api/views/mtfm-rxf4/rows.csv?accessType=DOWNLOAD',
  '2011': 'https://health.data.ny.gov/api/views/pyhr-5eas/rows.csv?accessType=DOWNLOAD',
  '2012': 'https://health.data.ny.gov/api/views/u4ud-w55t/rows.csv?accessType=DOWNLOAD',
  '2013': 'https://health.data.ny.gov/api/views/npsr-cm47/rows.csv?accessType=DOWNLOAD',
  '2014': 'https://health.data.ny.gov/api/views/rmwa-zns4/rows.csv?accessType=DOWNLOAD',
  '2015': 'https://health.data.ny.gov/api/views/82xm-y6g8/rows.csv?accessType=DOWNLOAD',
}

renames = {
  'Facility ID': 'Facility Id',
  'Payment Typology 1': 'Source of Payment 1',
  'Payment Typology 2': 'Source of Payment 2',
  'PaymentTopology 2': 'Source of Payment 2',
  'Payment Topology 3': 'Source of Payment 3',
}

converters = {
  'Operating Certificate Number': int_,
  'Facility Id': int_,
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
    df_year = read_csv_cached(resource, converters=converters)
    year_renames = {k: v for k, v in renames.items() if k in df_year.columns}
    if year_renames:
      df_year = df_year.rename(columns=year_renames)
    df_year['Year'] = int(year)
    df = pd.concat([df, df_year])

  print('Generating diagnosis.facility...')
  df[[
    'Facility Id',
    'Facility Name'
  ]].drop_duplicates().to_sql('diagnosis.facility', con, index=False, if_exists='replace')

  print('Generating diagnosis.ccs_diagnosis...')
  df[[
    'CCS Diagnosis Code',
    'CCS Diagnosis Description'
  ]].drop_duplicates().to_sql('diagnosis.ccs_diagnosis', con, index=False, if_exists='replace')

  print('Generating diagnosis.ccs_procedure...')
  df[[
    'CCS Procedure Code',
    'CCS Procedure Description'
  ]].drop_duplicates().to_sql('diagnosis.ccs_procedure', con, index=False, if_exists='replace')

  print('Generating diagnosis.arp_drg...')
  df[[
    'APR DRG Code',
    'APR DRG Description'
  ]].drop_duplicates().to_sql('diagnosis.arp_drg', con, index=False, if_exists='replace')

  print('Generating diagnosis.arp_mdc...')
  df[[
    'APR MDC Code',
    'APR MDC Description'
  ]].drop_duplicates().to_sql('diagnosis.arp_mdc', con, index=False, if_exists='replace')

  print('Generating diagnosis.arp_severity_of_illness...')
  df[[
    'APR Severity of Illness Code',
    'APR Severity of Illness Description'
  ]].drop_duplicates().to_sql('diagnosis.arp_severity_of_illness', con, index=False, if_exists='replace')

  print('Generating diagnosis.primary...')
  df.drop([
    'Facility Name',
    'CCS Diagnosis Description',
    'CCS Procedure Description',
    'APR DRG Description',
    'APR MDC Description',
    'APR Severity of Illness Description',
  ], axis=1).to_sql('diagnosis.primary', con, index=False, if_exists='replace')
