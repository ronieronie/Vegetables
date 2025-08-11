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





#localhost
# app.secret_key = 'supersecretkey'  # or use os.getenv('SECRET_KEY')
# username = os.getenv('MYSQLUSER', 'root')
# password = os.getenv('MYSQLPASSWORD', 'hElzjxVLpYsPkaiulbRTVpFQgHTvgaXz')
# host = os.getenv('MYSQLHOST', 'interchange.proxy.rlwy.net')
# port = os.getenv('MYSQLPORT', '15150')  # Railway port from your URL
# database = os.getenv('MYSQLDATABASE', 'railway')

app.secret_key = os.getenv('SECRET_KEY')
env = os.getenv("RAILWAY_ENV", "development")

host = os.getenv("MYSQLHOST") or ("mysql.railway.internal" if env == "production" else "interchange.proxy.rlwy.net")
port = os.getenv("MYSQLPORT") or ("3306" if env == "production" else "15150")
username = os.getenv("MYSQLUSER", "root")
password = os.getenv("MYSQLPASSWORD", "hElzjxVLpYsPkaiulbRTVpFQgHTvgaXz")
database = os.getenv("MYSQLDATABASE", "railway")

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

from market import routes


