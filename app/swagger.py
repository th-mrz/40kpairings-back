from flask import Blueprint
from flask_restplus import Api

from app.pairings import api as pairings_ns
from app.health import api as health_ns

blueprint = Blueprint('documented_api', __name__, url_prefix='/documented_api')

api_extension = Api(
    blueprint,
    title='Flask RESTplus Demo',
    version='1.0',
    description='Application tutorial to demonstrate Flask RESTplus extension\
        for better project structure and auto generated documentation',
    doc='/doc'
)

api_extension.add_namespace(pairings_ns)
api_extension.add_namespace(health_ns)
