from flask import session
from models import UserCredits

def get_team():
	team_id = session['slack_team']
	o = UserCredits.objects(team_id=team_id).first()
	return o