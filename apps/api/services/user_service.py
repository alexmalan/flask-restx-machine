"""Product related functions - services"""

from apps.api.models import User
from apps.extensions import bcrypt, db


def check_user_role(user=None):
    """
    Check user role type
    User has to have the role of a SELLER or BUYER

    :param User user: Found user
    """
    if user is None:
        return None

    user = User.query.filter_by(username=user.username).first()

    return user.role.value


def register_user(payload):
    """
    Register user using payload data

    :param dict payload: Request data payload
    """
    if payload is None or not isinstance(payload, dict):
        return False

    user = User.query.filter_by(username=payload["username"]).first()

    if user:
        return False

    hashed_password = bcrypt.generate_password_hash(payload["password"])
    payload["password"] = hashed_password
    new_user = User(**payload)

    db.session.add(new_user)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return True
