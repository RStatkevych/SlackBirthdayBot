# used as auth token in API call
# Read here for more info: https://api.slack.com/bot-users#custom_bot_users
BOT_TOKEN = ''

# channel ID where bot should send messages to
CHANNEL = ''

# Endpoint for API call to send message
ENDPOINT_URL = 'https://slack.com/api/chat.postMessage'

# Text for greating messsage
MSG_TEXT = '<!channel> HPBD {0} <@{1}>!'

# broker url for celery worker
BROKER_URL = 'mongodb://localhost:27017/birthday_bot'

# START : CELERY config
from celery import Celery
from celery.schedules import crontab

app = Celery('bot', broker=BROKER_URL)

app.conf.update(
	#setting cron schedule
	CELERYBEAT_SCHEDULE = {
	    'congrats_with_birthday': {
	        'task': 'bot.detect_birthday',
	        'schedule': crontab(hour=8, minute=0),
	    },
	}
)

CELERY_TIMEZONE = 'UTC'
# END : CELERY config