"""Actions related data transfer object"""

from flask_restx import Namespace


class ActionsDto:
    """Actions data transfer object definitions"""

    api = Namespace("action", description="Vending Machine related operations")
