import os

# grab the foder where tishscrip lives
basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'database.db'
USERNAME = 'admin'
PASSWORD = 'admin'
CSRF_ENABLE = True
SECRET_KEY = 'my_precious'

# define the full path for hte  database
DATABASE_PATH = os.path.join(basedir, DATABASE)

# the database uri
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH
