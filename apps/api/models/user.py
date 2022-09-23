"""User related model"""

import enum

from flask_login import UserMixin

from apps.extensions import db

from .audit import BaseModel


class UserRole(enum.Enum):
    """User roles enum definition"""

    SELLER = "SELLER"
    BUYER = "BUYER"


class User(BaseModel, UserMixin):
    """User database model"""

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    deposit = db.Column(db.Integer, nullable=False, default=0)
    role = db.Column(db.Enum(UserRole), default="BUYER")

    def __repr__(self):
        """User representation"""
        return f"{self.username} : {self.role}"
