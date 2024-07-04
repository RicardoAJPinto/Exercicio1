import gzip
import delegator
import os
import sys
from os import walk
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from dotenv import load_dotenv


load_dotenv() 

localhost: str = os.getenv('POSTGRES_HOST')
user: str = os.getenv('POSTGRES_USER')
db: str = os.getenv('POSTGRES_DB')
backup_days: int = os.getenv('CLEANUP_DAYS')
path_delete: str = os.getenv('PATH_DEL')

current_date = datetime.now()
delete_date = datetime.now() - timedelta(days=int(backup_days))

path = path_delete + 'bica-backup-' + current_date.strftime("%Y-%m-%d_%H%M") + '.gz'

with open("/secret.key", "rb") as key_file:
    key = key_file.read()

cipher_suite = Fernet(key)

with gzip.open(path, 'wb') as f:
  c = delegator.run('pg_dump -h ' + localhost + ' -U ' + user + db)
  encrypted_data = cipher_suite.encrypt(c.out.encode('utf-8'))
  f.write(encrypted_data)

try:
    cleanup = sys.argv[1]
except:
    cleanup = ''

if cleanup == 'clean':
    for (dirpath, dirnames, filenames) in walk(path_delete):
        print("teste")
        for filename in filenames:
            filetime = datetime.fromtimestamp(os.path.getctime(path_delete + filename))
            if filetime < delete_date:
                os.remove(path_delete + filename)