#!/usr/bin/env python3

from flask import (Blueprint, request, jsonify, abort, make_response)
from models.user import User
from models.notice import Notice
from models import storage

bp = Blueprint('notice', __name__, url_prefix='/api/v1')

@bp.route('/user/<user_id>/notice', methods=['POST'])
def create_notice(user_id):
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'title' not in request.get_json():
        abort(400, description="Missing title")

    if 'text' not in request.get_json():
        abort(400, description="Missing text")

    data = request.get_json()
    data["user_id"] = user_id
    instance = Notice(**data)
    instance.save()

    return make_response(jsonify(instance.to_dict()), 201)


@bp.route('/user/<user_id>/notices')
def get_user_notices(user_id):
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    notices = storage.all(Notice)
    print(notices)

    user_notices = []

    for notice in notices.values():
        if notice.user_id == user_id:
            user_notices.append(notice.to_dict())

    return make_response(jsonify(user_notices), 200)
