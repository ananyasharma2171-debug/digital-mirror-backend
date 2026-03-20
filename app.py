from flask import Flask
from flask_mysqldb import MySQL
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB')

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

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)