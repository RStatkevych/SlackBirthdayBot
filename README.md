# SlackBirthdayBot
Sends birthday congrats to the certain channel in slack team

Reads the 'birthday.csv' file, and if any birthday occurs, sends the message from one of the existing in 'congrats.txt' to channel that is specificated in CHANNEL variable of settings.py. BOT_TOKEN is also required

###To run celery worker:
 - celery -A bot worker
 - celery -A bot beat

###To launch supervisor daemon:
Edit necessary fields in supervisord.conf and then do
```
 sudo supervisord -c PATH_TO_YOUR_APP/supervisord.conf
```
