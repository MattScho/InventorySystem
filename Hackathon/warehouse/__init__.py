from flask import Flask
from warehouse.routes.backend import Backend
from flask_login import LoginManager
from flask_pymongo import PyMongo

# Initializes Flask
app = Flask(__name__, template_folder="./template")
app.config["MONGO_URI"] = "mongodb://127.0.0.1/SmartHouse"
db = PyMongo(app)

db.init_app(app)
Backend = Backend(db)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


from user import User

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User(int(user_id))

from warehouse.routes.main import main
# Registers the paths for the main component
app.register_blueprint(main)

from warehouse.routes.auth import auth
# Registers the paths for the authentication components
app.register_blueprint(auth)
