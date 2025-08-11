from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
import os
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
# app.config['SECRET_KEY'] = '1e32f81eb715404d20b202fd'
# db = SQLAlchemy(app)
# bcrypt = Bcrypt(app)
# login_manager = LoginManager(app)
# login_manager.login_view = "login_page"
# login_manager.login_message_category = "info"


app.secret_key = 'supersecretkey'


username = os.getenv('MYSQLUSER', 'root')
password = os.getenv('MYSQLPASSWORD', 'hElzjxVLpYsPkaiulbRTVpFQgHTvgaXz')
host = os.getenv('MYSQLHOST', 'localhost')
port = os.getenv('MYSQLPORT', '3306')  # default MySQL port
database = os.getenv('MYSQLDATABASE', 'railway')  # replace 'railway' with your actual DB name

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

from market import routes


