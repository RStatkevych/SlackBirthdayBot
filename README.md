# SlackBirthdayBot
Sends birthday congrats to the certain channel in slack team

Reads the 'birthday.csv' file, and if any birthday occurs, sends the message to channel that is specificated in CHANNEL variable of settings.py. BOT_TOKEN is also required

To run celery worker:
 - celery -A bot worker
 - celery -A bot beat
