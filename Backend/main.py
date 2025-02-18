from flask import Flask, jsonify, request, abort
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from flask_migrate import Migrate
from sqlalchemy import inspect
from flask_cors import CORS
from functools import wraps
from Routes import blueprints as bp
from config import config
from Database import db
import cloudinary
import os
from dotenv import load_dotenv
load_dotenv()

cloudinary.config(
  cloud_name = os.getenv('Cloud_name'),
  api_key = os.getenv('API_key'),
  api_secret = os.getenv('API_secret')
)

app = Flask(__name__)
app.config.from_object(config)
# api = Api(app)
CORS(app)
db.init_app(app)


# db = SQLAlchemy(app)

app.register_blueprint(bp[0], url_prefix='/auth')
app.register_blueprint(bp[1], url_prefix='/product')



@app.route('/')
def start():
    return "<h1>START</h1>"

# with app.app_context():
#     db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

# DATABASE_URL = app.config["SQLALCHEMY_DATABASE_URI"]

# print(f"Database URL: {DATABASE_URL}")