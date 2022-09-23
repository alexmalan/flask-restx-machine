"""
Base class for testing
"""
import unittest

import pytest

from app import create_app, db
from apps.api import blueprint, models


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment
        """
        self.app = create_app("testing")
        self.app.register_blueprint(blueprint)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()
        self.generic_setup()

    def tearDown(self):
        """
        Tear down the test environment
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    @staticmethod
    def generic_setup():
        """
        Generic setup to have:
        - 2 products to use in all unit tests;
        - 3 users to use in all unit tests;

        Can be used in all unit tests:
        -   product_id=200;
        -   product_id=201;
        -   user_id=100;
        -   user_id=101;
        -   user_id=102;
        """

        # Save user 0 - BUYER
        user_dict = dict(
            id=100,
            username="user0_buyer",
            password="Test1234",
            role="BUYER",
        )
        user = models.User(**user_dict)
        db.session.add(user)
        db.session.commit()

        # Save user 1 - SELLER
        user_dict = dict(
            id=101,
            username="user1_seller",
            password="Test1423",
            role="SELLER",
        )
        user = models.User(**user_dict)
        db.session.add(user)
        db.session.commit()

        # Save user 2 - SELLER
        user_dict = dict(
            id=102,
            username="user2_seller",
            password="Test6543",
            role="SELLER",
        )
        user = models.User(**user_dict)
        db.session.add(user)
        db.session.commit()

        # Save product 1 - Diet Coke
        prod_dict = dict(
            id=200,
            amountAvailable=20,
            cost=10,
            productName="Diet Coke",
            sellerId=101,
        )
        product = models.Product(**prod_dict)
        db.session.add(product)
        db.session.commit()

        # Save product 2 - Sprite
        prod_dict = dict(
            id=201,
            amountAvailable=40,
            cost=5,
            productName="Sprite",
            sellerId=102,
        )
        product = models.Product(**prod_dict)
        db.session.add(product)
        db.session.commit()
