# coding: utf-8

from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)

from ..models import (
    DBSession,
    User,
)


def user_factory(username, email, password):
    user = User()
    user.username = username
    user.email = email
    user.password = generate_password_hash(password)
    return user


def create_user(username, email, password):
    user = user_factory(username, email, password)
    DBSession.add(user)
    return user


def get_by_username(username):
    return DBSession.query(User).filter_by(username=username).first()


def auth_groupfinder(username, request):
    user = request.user
    if user is not None:
        return user.groups
    return None


def check_password(user, password):
    return check_password_hash(user.password, password)


def list_users():
    return DBSession.query(User).all()


def delete_user(username):
    user = get_by_username(username)
    DBSession.delete(user)
