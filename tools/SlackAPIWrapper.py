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

	@staticmethod
	def auth_redirect_handler(code):
		
		params = {
			'client_id': SLACK_APP_ID,
			'client_secret': SLACK_APP_SECRET,
			'code':code,
			'redirect_uri': SLACK_APP_REDIRECT_URI
		}

		return json.loads(requests.get(SlackAPIWrapper.__oauth_urls['OAUTH_ACCESS_TOKEN'], params=params).text)

	@staticmethod	
	def get_team():
		team_id = session['slack_team']
		o = UserCredits.objects(team_id=team_id).first()
		return o
	
	@staticmethod
	def check_user(access_token):
		user = json.loads(requests.get(SlackAPIWrapper.__oauth_urls['OAUTH_TEST_URL'], params={'token': access_token}).text)
		user_id = user['user_id']

		user_info = requests.get(SlackAPIWrapper.__oauth_urls['OAUTH_USER_INFO'], params={'token':access_token,'user': user_id})
		user_info = json.loads(user_info.text)['user']
		print user_info
		return user_info['is_admin'] == True or user_info['is_owner'] == True

	@property
	def authentication_url():
		return SlackAPIWrapper.__oauth_urls['OAUTH_AUTHENTICATION_URL']+('?scope=identify&client_id=%s' % (SLACK_APP_ID))

	@staticmethod
	def authorized(f):
		@wraps(f)
		def _(*args, **kwargs):
			if 'slack_team' in session:
				team_id = session['slack_team']
				o = UserCredits.objects(team_id=team_id).first()
				
				if SlackAPIWrapper.check_user(o.slack_access_token):
					return f()  
				else:
					return jsonify(**{'fail':True})
			else:
				return redirect(SlackAPIWrapper.authentication_url)
		return _