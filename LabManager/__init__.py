from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = 'changeme' # Mandatory to change this on deploy
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///app.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "auth.logon"
login_manager.login_message = "This page is restricted. Please login to access."

# These imports below will avoid circular imports
from LabManager.auth.routes import auth
from LabManager.main.routes import main
from LabManager.personnel.routes import personnel
from LabManager.equipments.routes import equipments
from LabManager.fieldtrips.routes import fieldtrips
from LabManager.notices.routes import notices
from LabManager.calendar.routes import calendar
from LabManager.news.routes import news

app.register_blueprint(auth)
app.register_blueprint(main)
app.register_blueprint(personnel)
app.register_blueprint(equipments)
app.register_blueprint(fieldtrips)
app.register_blueprint(notices)
app.register_blueprint(calendar)
app.register_blueprint(news)
