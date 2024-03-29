from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from .config import Settings
from flask import Flask


app = Flask(__name__)
db = SQLAlchemy()
bcrypt = Bcrypt(app)
jwt = JWTManager()
settings = None
ROOT = None


def create_app():
  from .config import Config
  cfg = Config()
  global ROOT
  ROOT = cfg.ROOT
  app.config.from_object(cfg)
  global settings
  settings = Settings()
  settings.root = cfg.ROOT
  settings.add_credentials(cfg.CREDENTIALS)
  db.init_app(app)
  
  from .views import auth, api
  app.register_blueprint(auth, url_prefix='/auth')
  app.register_blueprint(api, url_prefix='/api')

  jwt.init_app(app)

  from .models import Users

  @jwt.expired_token_loader
  def expired_token_callback(_jwt_header, jwt_payload):
    return {'msg': 'THE'}, 401
  
  @jwt.invalid_token_loader
  def invalid_token_callback(reason):
    return {'msg': 'TNF'}, 401
  
  @jwt.user_lookup_loader
  def user_lookup_callback(_jwt_header, jwt_payload):
    iden = jwt_payload['sub']
    return Users.query.filter_by(username=iden).one_or_none()
  
  from .functions import initial_user

  with app.app_context():
    db.create_all()
    if settings.SPAWN_ADMIN:
      initial_user(settings.ADMIN_CREDENTIALS)
  
  return app
