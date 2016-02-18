from flask import *
import requests
from slackbot_credits import *
from models import *
from tools import *
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'random-string'

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/auth/slack')
def slack_auth_redirect():
	code = request.args['code']

	response = slack.auth_redirect_handler(code)

	if not slack.check_user(response['access_token']):
		# TODO: handle with 404 page
		return jsonify(**{'lol':'fail'})

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
	
	return redirect(google_api.oauth_url())

@app.route('/auth/google')
def google_auth_redirect():
	code = request.args['code']
	team_id = session['slack_team']

	response = google_api.auth_redirect_handler(code)

	o = UserCredits.objects(team_id=team_id)
	
	if len(o) != 0:
		if 'refresh_token' in response:
			o.update(google_refresh_token=response['refresh_token'],
					 google_access_token=response['access_token'])
		else:
			o.update(google_access_token=response['access_token'])

	return redirect('/select_calendar')

@app.route('/select_calendar')
@slack.authorized
def function():
	team = slack.get_team()
	wrapper = google_api({'access_token': team.google_access_token})
	ls = wrapper.get_calendar_list()['items']
	# TODO: make RESTful ??
	return render_template('choose_calendar.html',calendars=ls)

if __name__ == '__main__':
    app.run(debug=True)
