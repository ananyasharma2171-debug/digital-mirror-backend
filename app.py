from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config.from_pyfile('config.py')

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
    app.run(host='0.0.0.0', port=5000)