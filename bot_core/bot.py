# -*- coding utf-8 -*-
import requests, datetime, csv, random, models, tools

from tools import *
from settings import *

@app.task
def detect_birthday():
    credits = models.Team.objects
    for credit in credits:
        congrats = models.Congrats.objects(team=credit)
        callendar = google_api(credit)
        import ipdb; ipdb.set_trace()
        birthdays = callendar.get_events(credit['calendar_id'])

        for birthday in birthdays:
            random_num = random.randint(0,len(congrats)-1)
            text = (birthday['summary'])
            slack.send_message(credit, congrats[random_num].text.format(text))

if __name__ == '__main__':
    detect_birthday()
