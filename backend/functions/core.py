from backend.exceptions import ValidationError
import secrets
import string

def create_uid(length, uids):
  alp = string.ascii_letters + string.digits
  while True:
    uid = ''.join(secrets.choice(alp) for _ in range(length))
    if uid not in uids:
      return uid
    

def initial_user(creds):
  from backend.models import Users

  user = Users.query.filter_by(username=creds['username']).first()
  if not user:
    creds['reg_ip'] = '127.0.0.1'
    try:
      user = Users(**creds)
      print(f'Пользователь {creds["username"]} успешно создан!')
    
    except ValidationError as valid:
      print(valid.message)

