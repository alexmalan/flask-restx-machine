"""
Action related functions - services
"""

from apps.api.models import Product
from apps.extensions import db


def buy_product(payload=None, user=None):
    """
    Buy product using payload data
    User has to have the role of a BUYER

    :param dict payload: Request data payload
    :param User user: Found user
    """
    if payload is None or not isinstance(payload, dict):
        return False, False, False

    # retrieve the product
    product = Product.query.filter_by(id=payload["product_id"]).first()

    if product:
        spending = product.cost * payload["quantity"]

        # check if the amount is enough
        if product.amountAvailable < payload["quantity"]:
            return False, False, False

        # check if the user has enough money
        if user.deposit < spending:
            return False, False, False

        # update the product amount
        if product.amountAvailable == payload["quantity"]:
            product.amountAvailable = 0
        else:
            product.amountAvailable -= payload["quantity"]

        # update the user deposit
        user.deposit -= spending
        change = user.deposit

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

        return change, spending, product


def deposit_amount(payload=None, user=None):
    """
    Deposit amount using payload data
    User has to have the role of a BUYER

    :param dict payload: Request data payload
    :param User user: Found user
    """
    if user.role.value != "BUYER":
        return False

    if payload is None or not isinstance(payload, dict):
        return False

    if not isinstance(payload.get("amount"), int):
        return False

    if payload.get("amount") not in [5, 10, 20, 50, 100]:
        return False

    if user:
        user.deposit += payload["amount"]

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

        return True
    return False


def reset_deposit(user=None):
    """
    Reset user deposit
    User has to have the role of a BUYER

    :param User user: Found user
    """
    if user:
        user.deposit = 0

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

        return True
    return False
