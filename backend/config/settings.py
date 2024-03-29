import yaml
import sys
import os


class Settings:
  ROOT = None
  STORAGE = None
  extra = dict()

  def _load_settings(self) -> None:
    fp = os.path.join(self.ROOT, 'config', 'settings.yaml')
    self.STORAGE = os.path.join(self.ROOT, 'storage')

    try:
      with open(fp, 'r', encoding='utf-8') as file:
        data: dict = yaml.safe_load(file)
      for name, option in data.items():
        if name.startswith('_'):
          self.extra[name.replace('_', '')] = option
        else:
          self.__dict__[name] = option
    except FileNotFoundError:
      print('Settings file not found!')
      sys.exit(-1)
  
  @property
  def root(self):
    return self.ROOT
  
  @root.setter
  def root(self, path):
    self.ROOT = path
  
  def add_credentials(self, creds):
    self._load_settings()
    self.ADMIN_CREDENTIALS = creds
