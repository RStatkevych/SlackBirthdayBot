# -*- coding utf-8 -*-
import requests
import datetime
import csv
import random

from settings import *

@app.task
def detect_birthday():
	today = datetime.date.today()
	with open('congrats.txt') as congrat:
		congrats = [line for line in congrat]
	
	with open('birthday.csv') as csvfile:
		reader = csv.reader(csvfile, quotechar='"')

		# ignoring first line
		reader.next()
		for line in reader:
			birthday = line[0]
			birthday = datetime.datetime.strptime(line[1], '%Y-%m-%d')
			random_num = random.randint(1, len(congrats)/2)

			if birthday.month == today.month and birthday.day == today.day:
				print(random_num)
				if line[3] == 'F':
					text = congrats[random_num*2-1].format(line[2],line[0])
				else:
					text = congrats[random_num*2-2].format(line[2],line[0])

				requests.post(ENDPOINT_URL, params={
					'text': text,
					'as_user': True,
					'channel': CHANNEL,
					'token': BOT_TOKEN
				})


if __name__ == '__main__':
	detect_birthday()