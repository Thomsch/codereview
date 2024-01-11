from flask import Flask
from flask_cors import CORS
import logging

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.logger.addHandler(logging.StreamHandler())
app.logger.setLevel(logging.INFO)

@app.route('/')
def home():
    return "Hello World"

@app.route('/about')
def about():
    return 'About'