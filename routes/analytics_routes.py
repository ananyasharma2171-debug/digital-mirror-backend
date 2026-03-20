from flask import Blueprint
from services.analytics_service import (
    calculate_life_lost,
    calculate_money_lost,
    calculate_future_projection
)

analytics = Blueprint('analytics', __name__)

def init_mysql(mysql_instance):
    global mysql
    mysql = mysql_instance


@analytics.route('/life-lost/<int:user_id>', methods=['GET'])
def life_lost(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT hours FROM user_usage WHERE user_id=%s", (user_id,))
    data = cur.fetchall()

    return calculate_life_lost(data)


@analytics.route('/money-lost/<int:user_id>/<int:rate>', methods=['GET'])
def money_lost(user_id, rate):
    cur = mysql.connection.cursor()
    cur.execute("SELECT hours FROM user_usage WHERE user_id=%s", (user_id,))
    data = cur.fetchall()

    return calculate_money_lost(data, rate)


@analytics.route('/future-projection/<int:user_id>/<int:years>/<int:rate>', methods=['GET'])
def future_projection(user_id, years, rate):
    cur = mysql.connection.cursor()
    cur.execute("SELECT hours FROM user_usage WHERE user_id=%s", (user_id,))
    data = cur.fetchall()

    return calculate_future_projection(data, years, rate)

@analytics.route('/daily-average/<int:user_id>', methods=['GET'])
def daily_average(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT hours FROM user_usage WHERE user_id=%s", (user_id,))
    data = cur.fetchall()

    if not data:
        return {"average": 0}

    total = sum([row[0] for row in data])
    avg = total / len(data)

    return {"daily_average_hours": round(avg, 2)}