"""
Product related model
"""
from apps.extensions import db

from .audit import BaseModel


class Product(BaseModel):
    """
    Product database model.
    Used for storing product details.
    """

    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amountAvailable = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Integer, nullable=False, default=0)
    productName = db.Column(db.String(255), nullable=False)
    sellerId = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        """
        Product representation
        """
        return self.productName
