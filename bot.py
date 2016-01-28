# -*- coding utf-8 -*-
import requests
import datetime
import csv
import random
import models
from CalendarAPIWrapper import *

from settings import *

@app.task
def detect_birthday():
	with open('congrats.txt') as congrat:
		congrats = [line for line in congrat]
	
	TEST_CREDITS = models.UserCredits.objects[0]
	callendar = CalendarAPIWrapper(TEST_CREDITS)
	birthdays = callendar.get_events(TEST_CREDITS['calendar_id'])

	for birthday in birthdays:
		random_num = random.randint(0,len(congrats))
		text = congrats[random_num*2-2].format(birthday['summary'])

		requests.post(ENDPOINT_URL, params={
			'text': text,
			'as_user': True,
			'channel': CHANNEL,
			'token': BOT_TOKEN
		})


if __name__ == '__main__':
	#detect_birthday()
	app.conf.update(
		CELERYBEAT_SCHEDULE = {
		    'congrats_with_birthday': {
		        'task': 'bot.detect_birthday',
		        'schedule': crontab(minute='*'),
		    },
		}
	)