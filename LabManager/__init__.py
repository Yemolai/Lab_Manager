from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = 'changeme' #Mandatory to change this on deploy
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///app.db'
db = SQLAlchemy(app)

#This import come at the end to avoid circular imports
from LabManager import routes
