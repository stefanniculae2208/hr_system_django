from datetime import datetime

def calculate_age(date_of_birth):
    today = datetime.today()
    return today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))