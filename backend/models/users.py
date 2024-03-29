from flask_jwt_extended import create_access_token, create_refresh_token
from backend.exceptions import ValidationError
from backend.functions import create_uid
from backend import db, bcrypt, settings
from datetime import datetime as dt
import string
import re


class Users(db.Model):
  uid = db.Column(db.String(6), primary_key=True)
  username = db.Column(db.String(50), nullable=False, unique=True)
  email = db.Column(db.String(100), nullable=False, unique=True)
  password = db.Column(db.String(255), nullable=False)
  token = db.Column(db.String(32), nullable=True)
  avatar = db.Column(db.String(255), nullable=True)
  reg_date = db.Column(db.Integer, nullable=False, default=int(dt.now().timestamp()))
  last_date = db.Column(db.Integer, nullable=False)
  reg_ip = db.Column(db.String(15), nullable=False)
  last_ip = db.Column(db.String(15), nullable=False)

  def __init__(self, username: str, email: str, passwords: tuple, reg_ip: str,
               grant_token: bool = False, reg_date: int = None,) -> None:
    self.uid = create_uid(6, [a.uid for a in self.query.all()])
    self.username = self._validate_username(username)
    self.email = self._validate_email(email)
    self.password = self._validate_passwords(passwords)
    self.reg_ip = reg_ip
    self.reg_date = reg_date if reg_date else int(dt.now().timestamp())
    self.last_ip = reg_ip
    self.last_date = self.reg_date
    if grant_token:
      self.token = self._grant_token()
    db.session.add(self)
    db.session.commit()

  @property
  def base_info(self) -> dict:
    return dict(uid=self.uid, username=self.username, email=self.email)
  
  @property
  def json(self) -> dict:
    bi = self.base_info
    bi.update(dict(last_ip=self.last_ip, last_date=self.last_date, token=self.token, platform=self.platform, os=self.os))

  @classmethod
  def login(cls, username, password, last_ip, user_agent) -> dict:
    user = cls.query.filter_by(username=username).first()
    if not user:
      raise ValidationError('login', 'not_found')
    return user._login(password, last_ip, user_agent)

  @classmethod
  def refresh(cls, iden) -> str:
    return create_access_token(identity=iden, fresh=False)

  @staticmethod
  def _validate_passwords(passwords: tuple) -> bytes:
    p1, p2 = passwords
    pattern = rf'{settings.STRONG_PASSWORD_PATTERN}'
    if not p1 or not p2:
      raise ValidationError('register', 'password_absence')
    if p1 != p2:
      raise ValidationError('register', 'password_mismatch')
    if not re.match(pattern, p1) and p1 != 'admin':
      raise ValidationError('register', 'weak_password')
    return bcrypt.generate_password_hash(p1)

  def _validate_username(self, username) -> str:
    user = self.query.filter_by(username=username).first()
    alp = string.ascii_letters + string.digits + string.punctuation
    if user:
      raise ValidationError('register', 'username_exists')
    if len(username) < 5 and username != 'admin':
      raise ValidationError('register', 'short_username')
    for letter in username:
      if letter not in alp:
        raise ValidationError('register', 'lang')
    return username
  
  def _validate_email(self, email) -> str:
    email_exists = self.query.filter_by(email=email).first()
    pattern = rf'{settings.EMAIL_PATTERN}'
    if email_exists:
      raise ValidationError('register', 'email_exists')
    if not re.match(pattern, email):
      raise ValidationError('regiter', 'email_validity')
    return email
  
  def _login(self, password, last_ip, user_agent) -> dict:
    if not bcrypt.check_password_hash(self.password, password):
      raise ValidationError('register', 'password_mismatch')
    self.last_ip = last_ip
    self._is_new_user_agent(*self._parse_agent(user_agent))
    accs_token = create_access_token(self.username, fresh=True)
    rfsh_token = create_refresh_token(self.username)
    extra = dict(accs_token=accs_token, rfsh_token=rfsh_token)
    db.session.commit()
    return self.collect_info(**extra)
  
  def _grant_token(self) -> str:
    tokens = [a.token for a in self.query.all()]
    return create_uid(32, tokens)
  
  def collect_info(self, **kwargs) -> dict:
    info = self.base_info
    info.update(kwargs)
    return info
