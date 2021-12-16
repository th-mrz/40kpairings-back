### Setup python

Pré-requis : python3

python3 -m venv venv

. venv/bin/activate

export FLASK_APP=main.py

export FLASK_ENV=development

flask run

swagger : localhost:5000/documented_api/doc

### Setup docker

Pré-requis : docker

docker build --tag pairing .

docker run -p 5000:5000 pairing

swagger : 0.0.0.0:5000/documented_api/doc

Un exemple de JSON à envoyer en post est disponible dans example.json 