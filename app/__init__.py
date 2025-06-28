from flask import Flask
from config import Config

# initialize Flask app with config ref
app = Flask(__name__)

app.config.from_object(Config)

from app import routes
