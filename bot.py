import requests
import datetime
import csv

from settings import *

@app.task
def detect_birthday():
	today = datetime.date.today()
	
	with open('birthday.csv') as csvfile:
		reader = csv.reader(csvfile, quotechar='"')
		for line in reader:
			birthday = line[0]
			birthday = datetime.datetime.strptime(line[1], '%Y-%m-%d')
			print line

			if birthday.month == today.month and birthday.day == today.day:
				requests.post(ENDPOINT_URL, params= {
						'text': MSG_TEXT.format(line[0], line[2]),
						'as_user': True,
						'channel': CHANNEL,
						'token': BOT_TOKEN
					})


if __name__ == '__main__':
	detect_birthday()