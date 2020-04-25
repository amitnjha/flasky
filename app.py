from flask import Flask, render_template
from flask import request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from hello import NameForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'flasky-secret'

bootstrap = Bootstrap(app)
moment =  Moment(app)


@app.route('/')
def index():
    #print(request)
    form = NameForm()
    
    return render_template('index.html',form = form,agent = request.headers.get('User-Agent'), current_time = datetime.utcnow())


@app.route('/<name>/<id>')
def user(name,id=0):
    #print(app.url_map)
    return render_template('user.html', name = name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500



