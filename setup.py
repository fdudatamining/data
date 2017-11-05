import os
import sys
import importlib
import sqlalchemy

databases = {
  'test': 'sqlite:///test.sqlite3',
  'install': 'mysql+pymysql://root:%s@%s/datamining' % (os.environ.get('MYSQL_ROOT_PASSWORD', ''), os.environ.get('MYSQL_HOST', '127.0.0.1')),
}

db = sys.argv[1]
con = sqlalchemy.create_engine(databases.get(db, db), pool_recycle=1)

for root, dirs, files in os.walk('datamining'):
  for f in files:
    mod, ext = os.path.splitext(f)
    if ext == '.py':
      print('Processing datamining.%s...' % (mod))
      try:
        importlib.import_module('datamining.%s' % (mod)).create(con)
      except Exception as e:
        print('[ERROR: datamining.%s]: %s' % (mod, e))
