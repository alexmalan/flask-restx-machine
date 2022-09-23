"""
Product related endpoints
"""

from flask import request
from flask_login import current_user, login_required
from flask_restx import Resource

from apps.api.dto import ProductDto
from apps.api.models import User
from apps.api.services import (check_user_role, create_product, delete_product,
                               list_products, update_product)
from apps.api.utils import response_with
from apps.api.utils import responses as resp

api = ProductDto.api
_product = ProductDto.product


@api.route("/")
class ProductCollection(Resource):
    """
    Collection for root - / - endpoint

    Args:
        Resource (Object)

    Returns:
        json: data
    """

    @api.doc(
        "Product details",
        responses={
            200: ("product", _product),
            401: "Unauthorized",
            404: "Not found",
        },
        security="basicAuth",
    )
    @login_required
    def get(self):
        """
        Returns products.
        """
        products = list_products()

        if products:
            response = api.marshal(products, _product)
            return response_with(resp.SUCCESS_200, value={"response": response})
        return response_with(
            resp.BAD_REQUEST_400, value={"response": "No products found"}
        )

    @api.doc(
        "Create product",
        responses={
            201: ("product", _product),
            400: "Invalid payload",
            403: "Unauthorized",
        },
    )
    @login_required
    def post(self):
        """
        Creates a new product.
        """
        user = User.query.filter_by(username=current_user.username).first()

        user_role = check_user_role(user)
        if user_role != "SELLER":
            return response_with(
                resp.UNAUTHORIZED_403,
                value={"message": "You are not authorized to perform this action"},
            )

        payload = request.get_json()
        if user:
            product = create_product(payload, user)
            if product:
                response = api.marshal(product, _product)
                return response_with(resp.SUCCESS_201, value={"response": response})
        return response_with(resp.BAD_REQUEST_400, value={"response": "No user found"})

    @api.doc(
        "Update product",
        responses={
            201: ("product", _product),
            422: "Invalid payload",
            400: "Bad Request",
            403: "Unauthorized",
        },
    )
    @login_required
    def put(self):
        """
        Update a product.
        """
        user = User.query.filter_by(username=current_user.username).first()
        user_role = check_user_role(user)
        if user_role != "SELLER":
            return response_with(
                resp.UNAUTHORIZED_403,
                value={"message": "You are not authorized to perform this action"},
            )

        payload = request.get_json()
        product = update_product(payload, user)
        if product:
            response = api.marshal(product, _product)
            return response_with(resp.SUCCESS_201, value={"response": response})
        return response_with(
            resp.INVALID_INPUT_422,
            value={
                "response": "Product not found or you are not the owner of this product"
            },
        )

    @api.doc(
        "Delete product",
        responses={
            200: "Product deleted",
            400: "Bad Request",
            403: "Unauthorized",
            422: "Invalid input",
        },
    )
    @login_required
    def delete(self):
        """
        Returns product details
        """
        user = User.query.filter_by(username=current_user.username).first()
        user_role = check_user_role(current_user)

        if user_role != "SELLER":
            return response_with(
                resp.UNAUTHORIZED_403,
                value={"message": "You are not authorized to perform this action"},
            )

        payload = request.get_json()
        product = delete_product(payload, user)

        if product:
            return response_with(
                resp.SUCCESS_200, value={"data": "Product deleted successfully"}
            )
        return response_with(
            resp.INVALID_INPUT_422,
            value={
                "response": "Product not found or you are not the owner of this product"
            },
        )
