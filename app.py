from flask import Flask, render_template
from flask_session import Session
from os import urandom
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False 
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = urandom(24).hex()
Session(app)
csrf = CSRFProtect(app)
# every time app reloads a new csrf token is generated,
# so forms loaded before the reload will get invalid csrf token when submitted
# to avoid missing csrf token error
# include this in forms submitted with POST request
# <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
# for fetch request, include this in the <head> tag (in {% block styles %})
# <meta name="csrf-token" content="{{ csrf_token() }}">
# and include in the 'headers' section of the fetch request
# 'X-CSRF-TOKEN': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
# to exclude view function from csrf protection
# from app import app, csrf
# @csrf.exempt

from errors import *
from routes_Harini import *
from booking_sys.routes import booking_sys
app.register_blueprint(booking_sys, url_prefix='/bookings')
from rewards_Nas import *
from productsroutes_Sixuan import *
from chatbot_Kyarnyo import *
from routes_Feedbacks import *
from chatserver import *


@app.route('/')
def home():
    return render_template('home.html')

# $ flask --debug run
# $ source env/bin/activate
# (env)$ FLASK_ENV=development python app.py

