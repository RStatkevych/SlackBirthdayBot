import requests
import json
import models
import datetime

from slackbot_credits import *

class CalendarAPIWrapper(object):
	client_id = GOOGLE_CALENDAR_APP_ID
	client_secret = GOOGLE_CALENDAR_APP_SECRET
	redirect_uri = 'http://localhost:5000/auth/google'

	__oauth_urls = {
		'OAUTH_URL_REFRESH_TOKEN' : 'https://www.googleapis.com/oauth2/v4/token',
		'OAUTH_URL_TOKEN_VALIDATION' : 'https://www.googleapis.com/oauth2/v3/tokeninfo',
	}

	__callendar_urls = {
		'CALLENDAR_URL_GET_CALENDAR_LIST' : 'https://www.googleapis.com/calendar/v3/users/me/calendarList/',
		'CALLENDAR_URL_GET_EVENTS': 'https://www.googleapis.com/calendar/v3/calendars/{0}/events/'
	}

	def __init__(self, user_data):
		self.user_data = user_data
	
	def __validate_token_decorator(f):
		def _(*args, **kwargs):
			self = args[0]

			if(not self.check_token_status()):
				self.refresh_token()

			kwargs['headers'] = {
				'Authorization': 'Bearer '+self.user_data['access_token']
			}

			return f(*args, **kwargs)
		return _

	@staticmethod
	def oauth_url():
		google_url = 'https://accounts.google.com/o/oauth2/v2/auth?client_id=%s&scope=email profile https://www.googleapis.com/auth/calendar.readonly&response_type=code&redirect_uri=%s&access_type=offline'
		url = google_url % (CalendarAPIWrapper.client_id, CalendarAPIWrapper.redirect_uri)

		return url

	@staticmethod
	def get_oauth_secrets():
		return {
			'client_id':CalendarAPIWrapper.client_id,
			'client_secret':CalendarAPIWrapper.client_secret,
			'redirect_uri': CalendarAPIWrapper.redirect_uri
		}
	def check_token_status(self):
		response = requests.get(self.__oauth_urls['OAUTH_URL_TOKEN_VALIDATION'], 
					 			params={'access_token':self.user_data['access_token']},)

		response = json.loads(response.text)
		
		if 'error_description' in response:
			return False
		else:
			return True
	
	def refresh_token(self):
		params = {
			'grant_type':'refresh_token',
			'refresh_token': self.user_data['refresh_token'],
			'client_secret': self.client_secret,
			'client_id': self.client_id
		}

		response = requests.post(self.__oauth_urls['OAUTH_URL_REFRESH_TOKEN'], params=params)
		response = json.loads(response.text)
		self.user_data['access_token'] = response['access_token']
		self.user_data.save()

	@__validate_token_decorator
	def get_calendar_list(self, **kwargs):
		response = requests.get(url=self.__callendar_urls['CALLENDAR_URL_GET_CALENDAR_LIST'], headers=kwargs['headers'])

		response = json.loads(response.text)
		return response 

	@__validate_token_decorator
	def get_events(self, calendar_id, **kwargs):
		response = requests.get(url=self.__callendar_urls['CALLENDAR_URL_GET_EVENTS'].format(calendar_id), headers=kwargs['headers'])
		today = datetime.date.today().strftime('%Y-%m-%d')

		response = json.loads(response.text)
		birthdays = []

		for item in response['items']:
			if item['start']['date'] == today:
				birthdays.append({'start': item['start']['date'], 'summary': item['summary']})
				
		return birthdays

if __name__ == '__main__':
	TEST_CREDITS = models.UserCredits.objects[0]
	callendar = CalendarAPIWrapper(TEST_CREDITS)
	print callendar.get_events('of1q1gcca4deaom36veuq4pkr8@group.calendar.google.com')