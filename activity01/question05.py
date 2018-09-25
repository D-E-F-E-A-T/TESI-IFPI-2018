import requests
from flask import Flask, render_template, jsonify
from flask_cors import CORS
from random import randint
from flask_sqlalchemy import SQLAlchemy
from time import sleep
from collections import OrderedDict

# My LIB:

from libs.myurllib import *

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


#############################

OGOL = 'http://www.ogol.com.br/equipa.php?id=%s&search=1'

PESSTAT = 'https://pesstatsdatabase.com/PSD/Players.php?Club=%s&type=0' 

SOFIFA = 'https://sofifa.com/team/%s'

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    ogol_id = db.Column(db.Integer, unique=True, nullable=False)
    pesstat_id = db.Column(db.Integer, unique=True, nullable=False)
    sofifa_id = db.Column(db.Integer, unique=True, nullable=False)
    #
    stadium = db.Column(db.String(160), nullable=True)
    rival = db.Column(db.String(160), nullable=True)
    captain = db.Column(db.String(160), nullable=True)
    league = db.Column(db.String(160), nullable=True)
    
    def __init__(self, name, ogol_id, pesstat_id, sofifa_id):
        self.name = name
        self.ogol_id = ogol_id
        self.pesstat_id = pesstat_id
        self.sofifa_id = sofifa_id
        #self.get_from_ogol()
        #self.stadium = 'A'

    def get_from_sofifa(self):
        url = SOFIFA % (self.sofifa_id)
        soup = get_parsed(url)
    
    def get_from_pesstat(self):
        url = PESSTAT % (self.pesstat_id)
        soup = get_parsed(url)
        soup.find(id='info')

    def get_from_ogol(self):
        url = OGOL % (self.ogol_id)
        soup = get_parsed(url)

    def __repr__(self):
        return '<Team %r>' % self.name

    def asdict(self):
        result = OrderedDict()
        for key in self.__mapper__.c.keys():
            if getattr(self, key) is not None:
                result[key] = str(getattr(self, key))
            else:
                result[key] = getattr(self, key)
        return result
        

db.create_all()

db.session.commit()

#############################

# Fetch One:

@app.route('/team/<name>')
def random_number(name):
    response = db.session.query(Team).filter(Team.name == name).first()
    return jsonify(response.asdict())

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    try:
        t = Team(name='malaga', ogol_id = 45, pesstat_id = 29, sofifa_id = 573)
        db.session.add(t)
        db.session.commit()    
    except Exception as e:
        print('Error: %s' % (e))
    finally:
        return render_template("index.html")

#############################

if __name__ == '__main__':
    app.run(use_debugger=True,host='0.0.0.0',use_reloader=True)