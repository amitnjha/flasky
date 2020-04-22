from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
    print(request)
    return request.headers.get('User-Agent')


@app.route('/<name>/<id>')
def user(name,id=0):
    return '<h1>Hello World in a bug way {}</h1>'.format(id)

