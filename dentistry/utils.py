def create_active_code(number):
    import random
    code = random.randint(10**(number-1), (10**number)-1)
    return code

def send_sms(mobile_number, message):
    pass