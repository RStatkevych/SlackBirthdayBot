from flask import session
from models import UserCredits
from slackbot_credits import *

from functools import wraps

import json, requests

class SlackAPIWrapper(object):
	__oauth_urls =  {
		"OAUTH_AUTHENTICATION_URL":"https://slack.com/oauth/authorize",
		"OAUTH_TEST_URL":'https://slack.com/api/auth.test',
		"OAUTH_ACCESS_TOKEN":'https://slack.com/api/oauth.access',
		"OAUTH_USER_INFO": "https://slack.com/api/users.info"
	}
	__messaging_urls = {
		'POST_MESSAGE_URL' : 'https://slack.com/api/chat.postMessage',
		'GET_CHANNELS_LIST' : 'https://slack.com/api/channels.list'
	}

	@staticmethod
	def auth_redirect_handler(code):
		''' recieves the access_token from grant code
		'''		
		params = {
			'client_id': SLACK_APP_ID,
			'client_secret': SLACK_APP_SECRET,
			'code':code,
			'redirect_uri': SLACK_APP_REDIRECT_URI
		}

		return json.loads(requests.get(SlackAPIWrapper.__oauth_urls['OAUTH_ACCESS_TOKEN'], params=params).text)

	@staticmethod	
	def get_team():
		''' returns team of signed in user. Takes team id from session
		'''
		team_id = session['slack_team']
		o = UserCredits.objects(team_id=team_id).first()
		return o
	
	@staticmethod
	def check_user(access_token):
		''' checks the user permissions. Only admins and team owners 
			are allowed to perform operations
		'''
		user = json.loads(requests.get(SlackAPIWrapper.__oauth_urls['OAUTH_TEST_URL'], params={'token': access_token}).text)
		user_id = user['user_id']

		user_info = requests.get(SlackAPIWrapper.__oauth_urls['OAUTH_USER_INFO'], params={'token':access_token,'user': user_id})
		user_info = json.loads(user_info.text)['user']

		return user_info['is_admin'] == True or user_info['is_owner'] == True

	@property
	def authentication_url():
		return SlackAPIWrapper.__oauth_urls['OAUTH_AUTHENTICATION_URL']+('?scope=identify&client_id=%s' % (SLACK_APP_ID))

	@staticmethod
	def get_channels_list(client):
		response = requests.get(SlackAPIWrapper.__messaging_urls['GET_CHANNELS_LIST'], params={
			'token': client['slack_access_token']
		})
		response = json.loads(response.text)
		return response['channels']

	@staticmethod
	def send_message(client,text):
		requests.post(SlackAPIWrapper.__messaging_urls['POST_MESSAGE_URL'], params={
			'text': text,
			'as_user': True,
			# HARDCODED
			'channel': client['channel_id'],
			'token': client['bot_token']
		})

	@staticmethod
	def authorized(f):
		''' decorator for wrapping the endpoint with security rules 
		'''
		@wraps(f)
		def _(*args, **kwargs):
			if 'slack_team' in session:
				team_id = session['slack_team']
				o = SlackAPIWrapper.get_team()
				
				if SlackAPIWrapper.check_user(o.slack_access_token):
					return f()  
				else:
					return jsonify(**{'fail':True})
			else:
				return redirect(SlackAPIWrapper.authentication_url)
		return _