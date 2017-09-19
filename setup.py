import os
import sys
import importlib
import sqlalchemy

databases = {
  'test': 'sqlite:///test.sqlite3',
  'install': 'mysql://root:%s@127.0.0.1' % (os.environ['MYSQL_ROOT_PASSWORD']),
}

db = sys.argv[1]
con = sqlalchemy.create_engine(databases.get(db, db))
con.execute('create database if not exists datamining')
con.execute('use datamining')

for mod in reversed(['diagnosis', 'hospitals', 'practitioners']): # todo: programically find these
  print('Processing datamining.%s...' % (mod))
  importlib.import_module('datamining.%s' % (mod)).create(con)
