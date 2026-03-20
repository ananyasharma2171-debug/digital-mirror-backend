from flask import Flask
from flask_mysqldb import MySQL
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

#database configuration
app.config['MYSQL_HOST'] = os.environ.get('MYSQLHOST')
app.config['MYSQL_USER'] = os.environ.get('MYSQLUSER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQLPASSWORD')
app.config['MYSQL_DB'] = os.environ.get('MYSQLDB')
app.config['MYSQL_PORT'] = int(os.environ.get('MYSQLPORT', 3306))

mysql = MySQL(app)

# 🔥 Import routes
from routes.auth_routes import auth, init_mysql as auth_init
from routes.usage_routes import usage, init_mysql as usage_init
from routes.analytics_routes import analytics, init_mysql as analytics_init

# 🔗 Connect MySQL
auth_init(mysql)
usage_init(mysql)
analytics_init(mysql)

# 🔗 Register routes
app.register_blueprint(auth)
app.register_blueprint(usage)
app.register_blueprint(analytics)

@app.route('/')
def home():
    return "Backend Running 🚀"