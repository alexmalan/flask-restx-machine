"""Product related functions - services"""
from apps.api.models import Product
from apps.extensions import db

from .user_service import check_user_role


def list_products():
    """List products"""
    return Product.query.all()


def create_product(payload=None, user=None):
    """
    Create product using payload data
    User has to have the role of a SELLER

    :param dict payload: Request data payload
    :param User user: Found user
    """
    if payload is None or not isinstance(payload, dict) or user is None:
        return None

    user_role = check_user_role(user)
    if user_role != "SELLER":
        return None

    payload["sellerId"] = user.id
    product = Product(**payload)

    # Save product
    db.session.add(product)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return product


def update_product(payload=None, user=None):
    """
    Update product using payload data

    :param dict payload: Request data payload
    :param User user: Found user
    """
    if payload is None or not isinstance(payload, dict):
        return None

    product = Product.query.filter_by(
        id=payload["product_id"], sellerId=user.id
    ).first()
    if product:
        if payload.get("productName"):
            if not isinstance(payload["productName"], str):
                return None
        if payload.get("amountAvailable"):
            if not isinstance(payload["amountAvailable"], int):
                return None
        if payload.get("cost"):
            if not isinstance(payload["cost"], int):
                return None

        product.productName = payload["productName"]
        product.amountAvailable = payload["amountAvailable"]
        product.cost = payload["cost"]

        db.session.add(product)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return product


def delete_product(payload=None, user=None):
    """
    Delete product using payload data

    :param dict payload: Request data payload
    :param User user: Found user
    """
    if payload is None or not isinstance(payload, dict):
        return None

    product = Product.query.filter_by(
        id=payload["product_id"], sellerId=user.id
    ).first()

    if product:
        db.session.delete(product)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

        return product
    return None
