"""Actions tests"""
import json

import pytest

from apps.api.models import Product, User
from apps.api.services import buy_product, deposit_amount, reset_deposit
from apps.extensions import bcrypt
from tests.utils.base import BaseTestCase


class TestUserController(BaseTestCase):
    """Tests for user controller"""

    def test_user_register_success(self):
        """Test user register successfully"""
        user_dict = {"username": "usertest@gmail.com", "password": "Test1234"}

        resp = self.client.post(
            f"/api/user/register",
            content_type="application/json",
            data=json.dumps(user_dict),
        )

        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.get_json()["code"], "success")
        self.assertEqual(resp.get_json()["response"], "User created successfully")

        check_register = User.query.filter_by(username=user_dict["username"]).first()

        self.assertEqual(check_register.username, user_dict["username"])
        self.assertEqual(
            bcrypt.check_password_hash(check_register.password, user_dict["password"]),
            True,
        )

    def test_user_register_invalid_input(self):
        """Test user register with invalid input"""
        user_dict = {"username": 2, "password": "Test1234"}

        resp = self.client.post(
            f"/api/user/register",
            content_type="application/json",
            data=json.dumps(user_dict),
        )

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.get_json()["code"], "badRequest")
        self.assertEqual(
            resp.get_json()["response"], "User already exists or invalid input"
        )

    def test_user_login_success(self):
        """Test user login successfully"""
        user = User.query.all()
        user_dict = {"username": user[0].username, "password": "Test1234"}

        resp = self.client.post(
            f"/api/user/login",
            content_type="application/json",
            data=json.dumps(user_dict),
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["code"], "success")
        self.assertEqual(resp.get_json()["response"], "User logged in")

    def test_user_login_invalid_input(self):
        """Test user login with invalid input"""
        user_dict = {"username": 234, "password": "Test1234"}

        resp = self.client.post(
            f"/api/user/login",
            content_type="application/json",
            data=json.dumps(user_dict),
        )

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.get_json()["code"], "badRequest")
        self.assertEqual(resp.get_json()["response"], "Invalid username or password")

    def test_user_logout_success(self):
        """Test user logout successfully"""
        user = User.query.all()
        user_dict = {"username": user[0].username, "password": "Test1234"}

        resp = self.client.post(
            f"/api/user/login",
            content_type="application/json",
            data=json.dumps(user_dict),
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["code"], "success")
        self.assertEqual(resp.get_json()["response"], "User logged in")

        resp = self.client.post(
            f"/api/user/logout",
            content_type="application/json",
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["code"], "success")
        self.assertEqual(resp.get_json()["response"], "User logged out")

    def test_user_logout_no_user_logged_in(self):
        """Test user logout with no user logged in"""
        resp = self.client.post(
            f"/api/user/logout",
            content_type="application/json",
        )

        self.assertEqual(resp.status_code, 401)
        self.assertEqual(
            resp.get_json()["message"],
            "The server could not verify that you are authorized to access the URL requested. You either supplied the wrong credentials (e.g. a bad password), or your browser doesn't understand how to supply the credentials required.",
        )

    def test_user_status_logged_in(self):
        """Test check status on user logged in"""
        user = User.query.all()
        user_dict = {"username": user[0].username, "password": "Test1234"}

        resp = self.client.post(
            f"/api/user/login",
            content_type="application/json",
            data=json.dumps(user_dict),
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["code"], "success")
        self.assertEqual(resp.get_json()["response"], "User logged in")

        resp = self.client.get(f"/api/user/login")

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["code"], "success")
        self.assertEqual(user[0].username in resp.get_json()["response"], True)

    def test_user_status_not_logged_in(self):
        """Test check status on user not logged in"""
        resp = self.client.get(f"/api/user/login")

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.get_json()["code"], "badRequest")
        self.assertEqual(resp.get_json()["response"], "No user logged in")

    def test_user_remove_success(self):
        """Test removing current logged in user"""
        user = User.query.all()
        initial_username = user[0].username

        user_dict = {"username": initial_username, "password": "Test1234"}

        resp = self.client.post(
            f"/api/user/login",
            content_type="application/json",
            data=json.dumps(user_dict),
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["code"], "success")
        self.assertEqual(resp.get_json()["response"], "User logged in")

        resp = self.client.delete(
            f"/api/user/remove",
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["code"], "success")
        self.assertEqual(resp.get_json()["response"], "User Removed")

        user_check = User.query.filter_by(username=initial_username).first()
        self.assertEqual(user_check, None)

    def test_user_remove_while_no_logged_in_user(self):
        """Test removing function without being logged in"""
        resp = self.client.delete(
            f"/api/user/remove",
        )

        self.assertEqual(resp.status_code, 401)
        self.assertEqual(
            resp.get_json()["message"],
            "The server could not verify that you are authorized to access the URL requested. You either supplied the wrong credentials (e.g. a bad password), or your browser doesn't understand how to supply the credentials required.",
        )
