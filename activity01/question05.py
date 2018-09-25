
import requests
from flask import Flask, render_template, jsonify
from flask_cors import CORS
from random import randint
from flask_sqlalchemy import SQLAlchemy

class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        block_start_string='[[',
        block_end_string=']]',
        variable_start_string='%%',
        variable_end_string='%%',
        comment_start_string='<#',
        comment_end_string='#>',
    ))

app  = CustomFlask(__name__, template_folder = "./")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['DEBUG'] = True

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

db = SQLAlchemy(app)

db.create_all()

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    ogol_id = db.Column(db.Integer, unique=True, nullable=False)
    pesstat_id = db.Column(db.Integer, unique=True, nullable=False)
    sofifa_id = db.Column(db.Integer, unique=True, nullable=False)
    
    def __repr__(self):
        return '<Team %r>' % self.name

@app.route('/api/random')
def random_number():
    response = {
        'randomNumber': randint(1, 100)
    }
    return jsonify(response)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    #if app.debug:
    #    return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("index.html")

if __name__ == '__main__':
    app.run(use_debugger=True,host='0.0.0.0',use_reloader=True)