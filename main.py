from flask import Flask

from app.swagger import blueprint as swagger_endpoint

app = Flask(__name__)
app.config['RESTPLUS_MASK_SWAGGER'] = False
app.register_blueprint(swagger_endpoint)

if __name__ == "__main__":
    app.run()
