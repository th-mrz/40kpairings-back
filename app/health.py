from flask_restplus import Namespace, Resource

api = Namespace('health', 'Health endpoints')


@api.route('')
class Health(Resource):

    def get(self):
        return "Hello world"
