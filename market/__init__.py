from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
import os
from sqlalchemy import create_engine
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
username = os.getenv('MYSQLUSER')
password = os.getenv('MYSQLPASSWORD')
host = os.getenv('MYSQLHOST')
port = os.getenv('MYSQLPORT')  # Railway port from your URL
database = os.getenv('MYSQLDATABASE')

app.secret_key = os.getenv('SECRET_KEY')
# username = os.getenv('MYSQLUSER')
# password = os.getenv('MYSQLPASSWORD')
# host = os.getenv('MYSQLHOST')
# port = os.getenv('MYSQLPORT')  # Railway port from your URL
# database = os.getenv('MYSQLDATABASE')

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# username = os.getenv('MYSQLUSER')
# password = os.getenv('MYSQLPASSWORD')
# host = os.getenv('MYSQLHOST')
# port = os.getenv('MYSQLPORT')
# database = os.getenv('MYSQLDATABASE')

# uri = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
# engine = create_engine(uri, pool_pre_ping=True)

# try:
#     with engine.connect() as conn:
#         result = conn.execute("SELECT 1")
#         print("✅ Connected to MySQL:", result.scalar())
# except Exception as e:
#     print("Connection failed:", e)


db.init_app(app)

from market import routes


