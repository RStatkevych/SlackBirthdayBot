from flask import *
import requests
from slackbot_credits import *
from models import *
from tools import *
import json
from flask.ext.bower import Bower

app = Flask(__name__)

Bower(app)

# TODO: join all data receiving into one view

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

	user_data = slack.get_user_data(response['access_token'])
	
	team = Team.objects(team_id=user_data['team_id'])

	if len(team) == 0:
		team = Team(team_id=response['team_id'], team_name=response['team_name'],
				 	bot_token=response['bot']['bot_access_token'], bot_id=response['bot']['bot_user_id'])
		team.save()
	else: 
		if 'bot' in response:
			team.update(bot_token=response['bot']['bot_access_token'], bot_id=response['bot']['bot_user_id'])

	session['slack_team'] = response['team_id']
	session['slack_user'] = response['access_token']
	return redirect('/config')

@app.route('/auth/google')
def google_auth_redirect():
	code = request.args['code']
	team_id = session['slack_team']

	response = google_api.auth_redirect_handler(code)

	o = Team.objects(team_id=team_id)
	
	if len(o) != 0 :
		if 'refresh_token' in response:
			o.update(google_refresh_token=response['refresh_token'],
					 google_access_token=response['access_token'])
		else:
			o.update(google_access_token=response['access_token'])

	return redirect('/config')

@app.route('/api/profile')
@slack.authorized
def get_user_data():
	return slack.get_user_data(session['slack_user'])

@app.route('/config')
@slack.authorized
@google_api.authorized
def render_select_calendar_template():
	return render_template('config-template.html')

@app.route('/api/congrats', methods=['GET', 'POST', 'DELETE'])
@slack.authorized
def get_congrats():
	user = slack.get_user_data(session['slack_user'])
	team = Team.objects(team_id=user['team_id'])[0]
	
	if request.method == 'GET':
		congrats = Congrats.objects(team=team).as_pymongo()
		return jsonify(**{'congrats':map(lambda x: {'text': x['text'], 'id': str(x['_id'])}, congrats)})
	
	if request.method == 'POST':
		c = Congrats(team=team, text=request.json['text']).save()
		return jsonify(**{'_id': str(c.id), 'text': c['text']})

	if request.method == 'DELETE': 
		Congrats(id=request.args['id']).delete()
		return jsonify(**{'status': 'ok'})

@app.route('/api/update', methods=['POST'])
@slack.authorized
def update():
	team = slack.get_team()
	data = request.json
	team.update(**data)
		
	return jsonify(**{'status':'ok'})

@app.route('/api/calendar', methods=['POST', 'GET'])
@slack.authorized
def get_calendars():
	team = slack.get_team()
	wrapper = google_api(team)

	ls = {
		'calendars': wrapper.get_calendar_list()['items'],
		'selected': team['calendar_id'] if 'calendar_id' in team else None
	}
	
	return jsonify(**{'data': ls})

@app.route('/api/channel')
@slack.authorized
def get_channels():
	user = slack.get_user_data(session['slack_user'])
	channels = slack.get_channels_list(user)
	return jsonify(**{'data': channels})

if __name__ == '__main__':
    #app.run(debug=True)
	app.run(debug=True)