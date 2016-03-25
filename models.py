from mongoengine import *

connect('birthday_bot_data')

class Team(Document):
	calendar_id 			= StringField()
	team_id 				= StringField()
	channel_id 				= StringField()
	team_name 				= StringField()
	bot_token 				= StringField()
	bot_id 					= StringField()
	google_access_token 	= StringField()
	google_refresh_token 	= StringField()

class Congrats(Document):
	text 					= StringField()
	team 					= ReferenceField(Team)