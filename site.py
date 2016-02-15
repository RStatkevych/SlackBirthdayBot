from flask import *
import requests
from slackbot_credits import *
from models import *
from tools.CalendarAPIWrapper import *
from tools import get_team
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'random-string'

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/auth/slack')
def slack_auth_redirect():
	code = request.args['code']

	url = 'https://slack.com/api/oauth.access'
	params = {
		'client_id': SLACK_APP_ID,
		'client_secret': SLACK_APP_SECRET,
		'code':code,
		'redirect_uri': SLACK_APP_REDIRECT_URI
	}

	response = json.loads(requests.get(url, params=params).text)

	session['slack_team'] = response['team_id']

	o = UserCredits.objects(team_id=response['team_id'])
	if len(o) == 0:
		o = UserCredits(team_id=response['team_id'], team_name=response['team_name'],
						bot_token=response['bot']['bot_access_token'], bot_id=response['bot']['bot_user_id'],
						slack_access_token=response['access_token'])
		o.save()

	else:
		o = o[0]
		o.update(bot_token=response['bot']['bot_access_token'], bot_id=response['bot']['bot_user_id'],
				 slack_access_token=response['access_token'])
	
	return redirect(CalendarAPIWrapper.oauth_url())

@app.route('/auth/google')
def google_auth_redirect():
	code = request.args['code']
	url = 'https://www.googleapis.com/oauth2/v4/token'
	params = CalendarAPIWrapper.get_oauth_secrets()
	params['grant_type'] = 'authorization_code'
	params['code'] = code
	params['access_type'] = 'offline'

	team_id = session['slack_team']

	headers = {'Content-Type': 'application/x-www-form-urlencoded'}
	response = json.loads(requests.post(url, data=params, headers=headers).text)
	o = UserCredits.objects(team_id=team_id)
	
	if len(o) != 0:
		if 'refresh_token' in response:
			o.update(google_refresh_token=response['refresh_token'],
					 google_access_token=response['access_token'])
		else:
			o.update(google_access_token=response['access_token'])

	return redirect('/select_calendar')

@app.route('/select_calendar')
def function():
	team = get_team()
	wrapper = CalendarAPIWrapper({'access_token': team.google_access_token})
	ls = wrapper.get_calendar_list()
	return jsonify(**{'data': ls})

if __name__ == '__main__':
    app.run(debug=True)
