import random
import time

otp_storage = {}

def generate_otp():
    return str(random.randint(100000, 999999))

def save_otp(email, otp):
    otp_storage[email] = {
        "otp": otp,
        "time": time.time()
    }

def verify_otp(email, user_otp):
    data = otp_storage.get(email)

    if not data:
        return False

    # Expire after 5 minutes
    if time.time() - data["time"] > 300:
        return False

    return data["otp"] == user_otp