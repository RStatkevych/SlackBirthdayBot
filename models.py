from mongoengine import *

connect('birthday_bot_data')

class UserCredits(Document):
	slack_access_token = StringField()
	google_access_token = StringField()
	google_refresh_token = StringField()
	calendar_id = StringField()
	team_id = StringField()
	team_name = StringField()
	bot_token = StringField()
	bot_id = StringField()