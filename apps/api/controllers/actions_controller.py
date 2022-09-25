"""Action related endpoints"""

from flask import request
from flask_login import current_user, login_required
from flask_restx import Resource

from apps.api.dto import ActionsDto, ProductDto
from apps.api.models import User
from apps.api.services import (buy_product, check_user_role, deposit_amount,
                               reset_deposit)
from apps.api.utils import response_with
from apps.api.utils import responses as resp

api = ActionsDto.api


@api.route("/buy")
class BuyCollection(Resource):
    """
    Collection for /buy - endpoint

    Args:
        Resource (Object)

    Returns:
        json: data
    """

    @api.doc(
        "Buy action",
        responses={200: "Success", 400: "Invalid payload", 403: "Unauthorized"},
    )
    @login_required
    def post(self):
        """Buys a product."""
        # Get the current user ROLE
        user = User.query.filter_by(username=current_user.username).first()
        user_role = check_user_role(user)

        # check if the user is a BUYER
        if user_role != "BUYER":
            return response_with(
                resp.UNAUTHORIZED_403,
                value={"response": "You are not authorized to perform this action"},
            )

        # validate the payload
        payload = request.get_json()
        change, spending, product = buy_product(payload, user)

        if product:
            # return report
            product_marsh = api.marshal(product, ProductDto.product)
            report = {
                "change": change,
                "spending": spending,
                "product": product_marsh,
            }
            return response_with(resp.SUCCESS_200, value={"response": report})
        return response_with(
            resp.BAD_REQUEST_400,
            value={"response": "Product not found or not enough money"},
        )


@api.route("/deposit")
class DepositCollection(Resource):
    """
    Collection for /deposit - endpoint

    Args:
        Resource (Object)

    Returns:
        json: data
    """

    @api.doc(
        "Deposit coins",
        responses={
            201: "Deposit successful",
            422: "Invalid payload",
            403: "Unauthorized",
            400: "Bad request",
        },
    )
    @login_required
    def post(self):
        """Deposit coin amount."""
        user = User.query.filter_by(username=current_user.username).first()
        user_role = check_user_role(user)
        if user_role != "BUYER":
            return response_with(
                resp.UNAUTHORIZED_403,
                value={"response": "You are not authorized to perform this action"},
            )

        payload = request.get_json()
        deposit = deposit_amount(payload, user)
        if deposit:
            return response_with(
                resp.SUCCESS_201, value={"response": "Deposit successful"}
            )
        return response_with(
            resp.BAD_REQUEST_400,
            value={"response": "User not found or invalid coin type inserted"},
        )


@api.route("/reset")
class ResetCollection(Resource):
    """
    Collection for root /reset - endpoint

    Args:
        Resource (Object)

    Returns:
        json: data
    """

    @api.doc(
        "Deposit reset",
        responses={
            200: "Deposit reset successful",
            400: "Bad request",
            403: "Unauthorized",
        },
    )
    @login_required
    def post(self):
        """Reset deposit amount to 0."""
        # Get the current user ROLE
        user = User.query.filter_by(username=current_user.username).first()
        user_role = check_user_role(user)
        if user_role != "BUYER":
            return response_with(
                resp.UNAUTHORIZED_403,
                value={"message": "You are not authorized to perform this action"},
            )

        reset = reset_deposit(user)
        if reset:
            return response_with(
                resp.SUCCESS_201, value={"response": "Deposit reset successfully"}
            )
        return response_with(
            resp.BAD_REQUEST_400, value={"response": "Deposit reset failed"}
        )
