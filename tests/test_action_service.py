from apps.api.models import Product, User
from apps.api.services import buy_product, deposit_amount, reset_deposit
from tests.utils.base import BaseTestCase


class TestActionController(BaseTestCase):
    # #######################################################
    # # BUY
    # #######################################################
    def test_buy_product_success(self):
        """
        Test buying a product successfully
        """
        user = User.query.filter_by(id=100).first()
        deposit_amount({"amount": 100}, user)
        self.assertEqual(user.deposit, 100)

        payload = {"product_id": 201, "quantity": 1}
        product = Product.query.filter_by(id=payload["product_id"]).first()

        change, spent, product = buy_product(payload, user)
        self.assertEqual(product.cost * payload["quantity"], spent)
        self.assertEqual(change, user.deposit)

    def test_buy_product_wrong_user_type(self):
        """
        Test buy product with wrong user type - SELLER INSTEAD OF BUYER
        """
        user = User.query.filter_by(id=101).first()
        deposit_status = deposit_amount({"amount": 100}, user)
        self.assertEqual(user.deposit, 0)
        self.assertEqual(deposit_status, False)

        payload = {"product_id": 201, "quantity": 1}
        change, spent, product = buy_product(payload, user)

        self.assertEqual(spent, False)
        self.assertEqual(product, False)
        self.assertEqual(change, False)

    def test_buy_product_non_existent_product(self):
        """
        Test buying a product that does not exist
        """
        user = User.query.filter_by(id=100).first()
        deposit_status = deposit_amount({"amount": 100}, user)
        self.assertEqual(user.deposit, 100)

        payload = {"product_id": 4000, "quantity": 1}
        with self.assertRaises(TypeError):
            change, spent, product = buy_product(payload, user)

    # #######################################################
    # # DEPOSIT
    # #######################################################
    def test_deposit_success(self):
        """
        Test depositing successfully
        """
        user = User.query.filter_by(id=100).first()

        before_deposit = user.deposit
        deposit_amount({"amount": 100}, user)

        user_after = User.query.filter_by(id=100).first()
        after_deposit = user_after.deposit
        self.assertEqual(before_deposit, after_deposit - 100)

    def test_deposit_invalid_input(self):
        """
        Test depositing an invalid input number
        """
        user = User.query.filter_by(role="BUYER").first()
        user_id = user.id

        before_deposit = user.deposit
        deposit_status = deposit_amount({"amount": 1234}, user)

        self.assertEqual(deposit_status, False)

    def test_deposit_invalid_user_type(self):
        """
        Test depositing with an invalid user type
        """
        user = User.query.filter_by(role="SELLER").first()
        user_id = user.id

        before_deposit = user.deposit
        deposit_status = deposit_amount({"amount": 1234}, user)

        self.assertEqual(deposit_status, False)

    def test_deposit_invalid_input_instance_type(self):
        """
        Test depositing an invalid input instance type
        """
        user = User.query.filter_by(role="BUYER").first()
        user_id = user.id

        before_deposit = user.deposit
        deposit_status = deposit_amount({"amount": [1, 2, 33, 4]}, user)

        self.assertEqual(deposit_status, False)

    #######################################################
    # RESET
    #######################################################

    def test_reset_success(self):
        """
        Test resetting successfully
        """
        user = User.query.filter_by(role="BUYER").first()
        user_id = user.id

        before_deposit = user.deposit
        deposit_status = deposit_amount({"amount": 100}, user)
        user_after = User.query.filter_by(id=user_id).first()
        after_deposit = user_after.deposit
        self.assertEqual(before_deposit, after_deposit - 100)

        reset_deposit(user_after)

        user_after_reset = User.query.filter_by(id=user_id).first()
        self.assertEqual(user_after_reset.deposit, 0)
