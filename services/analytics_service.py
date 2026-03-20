def calculate_life_lost(data):
    total_hours = sum([row[0] for row in data])

    days_lost = total_hours / 24
    months_lost = days_lost / 30

    return {
        "total_hours": total_hours,
        "days_lost": round(days_lost, 2),
        "months_lost": round(months_lost, 2)
    }


def calculate_money_lost(data, rate):
    total_hours = sum([row[0] for row in data])

    return {
        "total_hours": total_hours,
        "rate_per_hour": rate,
        "money_lost": total_hours * rate
    }


def calculate_future_projection(data, years, rate):
    total_hours = sum([row[0] for row in data])

    avg_daily = total_hours / len(data) if data else 0
    yearly_hours = avg_daily * 365

    future_hours = yearly_hours * years
    days_lost = future_hours / 24
    money_lost = future_hours * rate

    return {
        "years": years,
        "projected_hours": round(future_hours, 2),
        "days_lost": round(days_lost, 2),
        "money_lost": round(money_lost, 2)
    }