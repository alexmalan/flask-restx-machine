"""User related data transfer object"""

from flask_restx import Namespace, fields


class UserDto:
    """User data transfer object definitions"""

    api = Namespace("user", description="User related operations")

    user = api.model(
        "User",
        {
            "username":
            fields.String(
                description="User username",
                required=True,
                attribute="username",
            ),
            "password":
            fields.String(description="User password",
                          required=True,
                          attribute="password"),
            "deposit":
            fields.Integer(description="User deposit", attribute="deposit"),
            "role":
            fields.String(description="User role", attribute="role"),
        },
    )
