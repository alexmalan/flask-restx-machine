"""User controller"""
from email_validator import validate_email
from flask import request
from flask_login import current_user, login_required, login_user, logout_user
from flask_restx import Resource

from apps.api.dto import UserDto
from apps.api.models import User
from apps.api.services import register_user
from apps.api.utils import response_with
from apps.api.utils import responses as resp
from apps.extensions import bcrypt, db, login_manager

api = UserDto.api
_user = UserDto.user


@api.route("/register")
class UserRegisterCollection(Resource):
    """
    Collection for root /register - endpoint

    Args:
        Resource (Object)

    Returns:
        json: data
    """

    @api.doc(
        "User registration",
        responses={
            201: "User registered successfully",
            400: "Bad request",
        },
    )
    @api.expect(_user)
    def post(self):
        """Register User"""
        payload = request.get_json()
        register = register_user(payload)
        if register:
            return response_with(
                resp.SUCCESS_201, value={"response": "User created successfully"}
            )
        return response_with(
            resp.BAD_REQUEST_400,
            value={"response": "User already exists or invalid input"},
        )


@api.route("/login")
@api.expect(_user)
class UserLoginCollection(Resource):
    """
    Collection for root /login - endpoint

    Args:
        Resource (Object)

    Returns:
        json: data
    """

    @login_manager.user_loader
    def load_user(user_id):
        """Check if user is logged in on every page load."""
        return User.query.get(int(user_id))

    @api.doc(
        "Login user",
        responses={
            200: "User logged in successfully",
            400: "Bad request",
            403: "Unauthorized",
        },
    )
    @api.expect(_user)
    def post(self):
        """Login user."""
        if current_user.is_authenticated:
            return response_with(
                resp.BAD_REQUEST_400,
                value={
                    "response": "There is already an active session using your account"
                },
            )
        payload = request.get_json()
        try:
            validate_email(payload["username"])
        except Exception:
            return response_with(
                resp.BAD_REQUEST_400,
                value={"response": "Invalid username or password"},
            )
        user = User.query.filter_by(username=payload["username"]).first()
        if user:
            if bcrypt.check_password_hash(user.password, payload["password"]):
                login_user(user)
                return response_with(
                    resp.SUCCESS_200, value={"response": "User logged in"}
                )
        return response_with(
            resp.BAD_REQUEST_400,
            value={"response": "Invalid username or password"},
        )

    @api.doc(
        "User status",
        responses={
            200: "User logged in",
            400: "Bad request",
        },
    )
    def get(self):
        """Returns user"""
        if current_user.is_anonymous or not current_user.is_authenticated:
            return response_with(
                resp.BAD_REQUEST_400, value={"response": "No user logged in"}
            )
        return response_with(
            resp.SUCCESS_200,
            value={"response": f"{current_user.username} : {current_user.role}"},
        )


@api.route("/logout")
class UserLogoutCollection(Resource):
    """
    Collection for root /logout - endpoint

    Args:
        Resource (Object)

    Returns:
        json: data
    """

    @api.doc(
        "Logout user",
        responses={
            200: "User logged out successfully",
            400: "Bad request",
        },
    )
    @login_required
    def post(self):
        """Logout user."""
        log_status = logout_user()
        if log_status:
            return response_with(
                resp.SUCCESS_200, value={"response": "User logged out"}
            )
        return response_with(
            resp.BAD_REQUEST_400, value={"response": "No user logged in"}
        )


@api.route("/remove")
class UserDeleteCollection(Resource):
    """
    Collection for root /remove - endpoint

    Args:
        Resource (Object)

    Returns:
        json: data
    """

    @api.doc(
        "Remove user",
        responses={
            200: "User removed successfully",
            400: "Bad request",
        },
    )
    @login_required
    def delete(self):
        """Remove current user from the system"""
        user = User.query.filter_by(username=current_user.username).first()

        if user:
            db.session.delete(user)
            db.session.commit()

            logout_user()

            return response_with(resp.SUCCESS_200, value={"response": "User Removed"})
        return response_with(resp.BAD_REQUEST_400, value={"response": "User not found"})
