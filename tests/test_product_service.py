from apps.api.models import Product, User
from apps.api.services import (create_product, delete_product, list_products,
                               update_product)
from tests.utils.base import BaseTestCase


class TestProductController(BaseTestCase):
    #######################################################
    # GET
    #######################################################
    def test_product_get_list(self):
        """
        Test getting a list of products
        """
        products_list = Product.query.all()
        products = list_products()

        self.assertEqual(len(products_list), len(products))

    #######################################################
    # POST
    #######################################################
    def test_product_create_wrong_user_type(self):
        """
        Test create product with wrong user type - BUYER INSTEAD OF SELLER
        """
        user = User.query.filter_by(id=100).first()

        product_dict = dict(
            amountAvailable=20,
            cost=10,
            productName="Diet Coke",
            sellerId=100,
        )

        product = create_product(product_dict, user)
        self.assertEqual(product, None)

    def test_product_create_wrong_input_type(self):
        """
        Test getting an author that does not exist raises 404
        """
        user = User.query.filter_by(id=100).first()

        product_dict = dict(
            amountAvailable=None,
            cost="10",
            productName="Diet Coke",
            sellerId=100,
        )

        product = create_product(product_dict, user)

        self.assertEqual(user.role.value, "BUYER")
        self.assertEqual(product, None)

    def test_product_create_success(self):
        """
        Test creating a new product
        """
        user = User.query.filter_by(id=101).first()

        product_dict = dict(
            amountAvailable=20,
            cost=10,
            productName="Sprite",
            sellerId=101,
        )

        product = create_product(product_dict, user)

        self.assertEqual(user.role.value, "SELLER")
        self.assertEqual(product.productName, product_dict["productName"])
        self.assertEqual(product.amountAvailable, product_dict["amountAvailable"])
        self.assertEqual(product.cost, product_dict["cost"])
        self.assertEqual(product.sellerId, product_dict["sellerId"])
        self.assertTrue(product)

    #######################################################
    # DELETE
    #######################################################
    def test_product_delete_success(self):
        """
        Test deleting a product
        """
        user = User.query.filter_by(id=101).first()

        product_dict = dict(
            amountAvailable=11,
            cost=1,
            productName="Sprites",
            sellerId=101,
        )

        product = create_product(product_dict, user)
        before_remove = len(Product.query.all())

        self.assertEqual(user.role.value, "SELLER")
        self.assertEqual(product.productName, product_dict["productName"])
        self.assertEqual(product.amountAvailable, product_dict["amountAvailable"])
        self.assertEqual(product.cost, product_dict["cost"])
        self.assertEqual(product.sellerId, product_dict["sellerId"])
        self.assertTrue(product)

        delete_product({"product_id": product.id}, user)
        self.assertEqual(product.productName, product_dict["productName"])

        after_remove = len(Product.query.all())
        self.assertEqual(before_remove, after_remove + 1)

    def test_product_delete_another_user_associated(self):
        """
        Test deleting a product that is not associated with the user
        """
        user = User.query.filter_by(id=101).first()

        product_dict = dict(
            amountAvailable=11,
            cost=1,
            productName="Sprites",
            sellerId=101,
        )

        product = create_product(product_dict, user)
        before_remove = len(Product.query.all())

        self.assertEqual(user.role.value, "SELLER")
        self.assertEqual(product.productName, product_dict["productName"])
        self.assertEqual(product.amountAvailable, product_dict["amountAvailable"])
        self.assertEqual(product.cost, product_dict["cost"])
        self.assertEqual(product.sellerId, product_dict["sellerId"])
        self.assertTrue(product)

        user2 = User.query.filter_by(id=102).first()

        removed = delete_product({"product_id": product.id}, user2)
        after_remove = len(Product.query.all())
        self.assertEqual(before_remove, after_remove)

    #######################################################
    # PUT
    #######################################################
    def test_product_update(self):
        """
        Test update product
        """
        user = User.query.filter_by(id=101).first()

        product_dict = dict(
            amountAvailable=11,
            cost=1,
            productName="Sprites",
            sellerId=101,
        )

        product = create_product(product_dict, user)

        self.assertEqual(user.role.value, "SELLER")
        self.assertEqual(product.productName, product_dict["productName"])
        self.assertEqual(product.amountAvailable, product_dict["amountAvailable"])
        self.assertEqual(product.cost, product_dict["cost"])
        self.assertEqual(product.sellerId, product_dict["sellerId"])
        self.assertTrue(product)

        new_payload = dict(
            product_id=product.id,
            amountAvailable=11,
            cost=1,
            productName="Testing update",
            sellerId=user.id,
        )
        updated = update_product(new_payload, user)
        self.assertEqual(updated.productName, new_payload["productName"])
        self.assertEqual(updated.amountAvailable, new_payload["amountAvailable"])
        self.assertEqual(updated.cost, new_payload["cost"])
        self.assertEqual(updated.sellerId, user.id)

    def test_product_update_another_user_associated(self):
        """
        Test updating a product that is not associated with the user
        """
        user = User.query.filter_by(id=101).first()

        product_dict = dict(
            amountAvailable=11,
            cost=1,
            productName="Sprites",
            sellerId=101,
        )

        product = create_product(product_dict, user)

        self.assertEqual(user.role.value, "SELLER")
        self.assertEqual(product.productName, product_dict["productName"])
        self.assertEqual(product.amountAvailable, product_dict["amountAvailable"])
        self.assertEqual(product.cost, product_dict["cost"])
        self.assertEqual(product.sellerId, product_dict["sellerId"])
        self.assertTrue(product)

        user2 = User.query.filter_by(id=102).first()

        user2_payload = dict(
            product_id=product.id,
            amountAvailable=11,
            cost=1,
            productName="Testing update",
            sellerId=102,
        )
        updated = update_product(user2_payload, user2)
        self.assertEqual(updated, None)
