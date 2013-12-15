from os.path import abspath, dirname, join
basedir = abspath(dirname(__file__))

STORAGE_CLASS = 'FileStorage'

FILESTORAGE_DIR = join(abspath(join(basedir, '../')), 'data')

# data more than this many seconds old will be marked as old
AGE_THRESHOLD_SEC = 86400
