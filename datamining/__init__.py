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