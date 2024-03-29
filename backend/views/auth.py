from flask_jwt_extended import jwt_required, current_user, get_jwt_identity
from flask import Blueprint, request as req, jsonify
from backend.exceptions import ValidationError
from backend.models import Users


auth = Blueprint('auth', __name__)


@auth.route('/', methods=['POST'])
def login():
  if req.method == 'POST':
    user_data = req.get_json()
    user_data['last_ip'] = req.remote_addr
    try:
      creds = Users.login(**user_data)
      return jsonify(dict(status='success', body=creds))
    except ValidationError as valid:
      return jsonify(valid.json), 400
    

@auth.route('/me', methods=['GET'])
@jwt_required()
def user_info():
  return jsonify(dict(status='success', granted=bool(current_user)))


@auth.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
  if req.method == 'POST':
    iden = get_jwt_identity()
    token = Users.refresh(iden)
    return jsonify(dict(status='success', token=token))


@auth.route('/logout')
@jwt_required()
def logout():
  return jsonify(dict(status='success', message='Вы успешно вышли из аккаунта.'))
