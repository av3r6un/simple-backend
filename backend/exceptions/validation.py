from .base import AHException


class ValidationError(AHException):
  def __init__(self, case, error, *args, **kwargs) -> None:
    super().__init__('validation', *args)
    self.make_error(case, error, **kwargs)


