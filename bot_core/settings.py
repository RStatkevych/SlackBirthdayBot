#!/usr/bin/python
# -*- coding: utf-8 -*-

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
	        'task': 'bot_core.bot.detect_birthday',
	        'schedule': crontab(minute='*'),
	    },
	}
)

CELERY_TIMEZONE = 'UTC'
# END : CELERY config
