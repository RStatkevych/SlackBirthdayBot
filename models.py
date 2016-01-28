from mongoengine import *

connect('birthday_bot_data')

class UserCredits(Document):
	access_token = StringField()
	refresh_token = StringField()
	calendar_id = StringField()