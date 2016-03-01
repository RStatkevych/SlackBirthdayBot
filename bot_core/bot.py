# -*- coding utf-8 -*-
import requests
import datetime
import csv
import random
import models
import tools
from tools import *

from settings import *

@app.task
def detect_birthday():
	with open('congrats.txt') as congrat:
		congrats = [line for line in congrat]
	credits = models.UserCredits.objects
	for credit in credits:

		callendar = google_api(credit)

		birthdays = callendar.get_events(credit['calendar_id'])

		for birthday in birthdays:
			random_num = random.randint(0,len(congrats))
			text = (birthday['summary'])
			slack.send_message(credit, text)


if __name__ == '__main__':
	detect_birthday()
	#slack.send_message({'channel_id':'C0507DDEW', 'bot_token':'xoxb-17855172657-4S3JQwZ2otTWA30kNeaCt9gq', 'as_user':True}, '<!channel> Сегодня день рождения у <@ydudar> (Ярослава Дударя)! Поздравляем его от имени колектива и желаем ему счастья и здорвья, а также творческих и професиональных успехов!')
