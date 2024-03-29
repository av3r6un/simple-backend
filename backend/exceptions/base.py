import yaml
import sys
import os


class AHException(BaseException):
  message = None

  def __init__(self, dep, *args) -> None:
    super().__init__(*args)

    self.messages = self._load_messages(dep)

  @staticmethod
  def _load_messages(dep):
    from backend import ROOT
    fp = os.path.join(ROOT, 'config', 'messages.yaml')
    try:
      with open(fp, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
      return data[dep]
    except FileNotFoundError:
      print('Exception messages file not found!')
      sys.exit(-1)
  
  def make_error(self, case, error, **kwargs):
    self.message = ' '.join(kwargs.get(word, word) for word in self.messages[case][error].split())

  @property
  def json(self):
    return dict(status='error', message=self.message)
