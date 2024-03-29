from flask_jwt_extended import jwt_required, current_user
from flask import Blueprint, jsonify, request as req
from backend.exceptions import ValidationError
from backend import settings


api = Blueprint('api', __name__)


@api.route('/', methods=['GET'])
def main():
  return jsonify(dict(ok=True))
