from os.path import abspath, dirname, join
basedir = abspath(dirname(__file__))

STORAGE_CLASS = 'FileStorage'

FILESTORAGE_DIR = join(abspath(join(basedir, '../')), 'data')

