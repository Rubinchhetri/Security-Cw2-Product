# from customer.models import Customer
from django.contrib import messages, auth
from django.contrib.auth.models import User



# def log_activity(user, activity):
def log_activity(user, activity):
    # user = auth.authenticate(username=username)
    if user.is_authenticated:
        try:
            username = user.get_username
        except User.DoesNotExist:
            username = 'Unknown'
    else:
        username = 'Anonymous'

    with open('activity_log.txt', 'a') as file:
        file.write(f"User: {username} | Activity: {activity}\n")
        # file.write(f"User: {username} | Activity:\n")