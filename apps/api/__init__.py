"""Flask app initialization"""

from flask import Blueprint
from flask_restx import Api

from apps.api.controllers import action_ns, product_ns, user_ns

blueprint = Blueprint("api", __name__, url_prefix="/api")

authorizations = {"basicAuth": {"type": "basic"}}

api = Api(
    blueprint,
    version="1.0",
    title="Flask Vending Machine",
    description="Flask Vending Machine",
    contact="Alex Malan",
    contact_email="alex@recoders.io",
    doc="/docs",
    authorizations=authorizations,
)

api.add_namespace(product_ns)
api.add_namespace(user_ns)
api.add_namespace(action_ns)
