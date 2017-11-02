import os
import sys
import importlib
import sqlalchemy

databases = {
  'test': 'sqlite:///test.sqlite3',
  'install': 'mysql+pymysql://root:%s@%s/datamining' % (os.environ['MYSQL_ROOT_PASSWORD'], os.environ.get('MYSQL_HOST', '127.0.0.1')),
}

db = sys.argv[1]
con = sqlalchemy.create_engine(databases.get(db, db))

for mod in reversed(['diagnosis', 'hospitals', 'practitioners']): # todo: programically find these
  print('Processing datamining.%s...' % (mod))
  importlib.import_module('datamining.%s' % (mod)).create(con)

