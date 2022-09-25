"""Product related data transfer object"""

from flask_restx import Namespace, fields


class ProductDto:
    """Product data transfer object definitions"""

    api = Namespace("product", description="Product related operations")

    product = api.model(
        "Product",
        {
            "id":
            fields.Integer(description="Product identifier"),
            "amountAvailable":
            fields.Integer(
                description="Product availability",
                required=True,
                attribute="amountAvailable",
            ),
            "cost":
            fields.Integer(
                description="Product cost", required=True, attribute="cost"),
            "productName":
            fields.String(description="Product name",
                          required=True,
                          attribute="productName"),
            "sellerId":
            fields.Integer(description="Product user",
                           required=True,
                           attribute="sellerId"),
        },
    )
