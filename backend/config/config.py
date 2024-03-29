from dotenv import load_dotenv
import yaml
import sys
import os


class Config:
  ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', '..')

  def __init__(self) -> None:
    load_dotenv(os.path.join(self.ROOT, 'config', '.env'))
    self.SECRET_KEY = os.environ.get('SECRET_KEY')
    self.JWT_SECRET_KEY = self.SECRET_KEY
    self._load_credentials(bool(os.environ.get('ADMIN_PRESENCE')))
    self._load_settings(os.path.join(self.ROOT, 'config', 'backend.yaml'))

  def _load_credentials(self, admin_presence: bool) -> None:
    self.CREDENTIALS = dict(
      username=os.environ.get('ADMIN_UNAME'), email=os.environ.get('ADMIN_EMAIL'),
      passwords=(os.environ.get('ADMIN_PSWD'), os.environ.get('ADMIN_PSWD')),
      grant_token=bool(os.environ.get('ADMIN_GT'))
    ) if admin_presence else None

  def _load_settings(self, path) -> None:
    try:
      with open(path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
      self.SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(self.ROOT, "backend", data.pop("DB_URI"))}'
      self.__dict__.update(data)
    except FileNotFoundError:
      print('Backend settings file not found!')
      sys.exit(-1)
  