import random

otp_storage = {}

def generate_otp(email):
    otp = str(random.randint(100000, 999999))
    otp_storage[email] = otp
    return otp

def verify_otp(email, user_otp):
    return otp_storage.get(email) == user_otp