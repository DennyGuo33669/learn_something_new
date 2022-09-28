from mongoengine import Document, IntField, StringField


class Users(Document):
	name = StringField(required=True, max_length=200)
	age = IntField(required=True)
	sex = StringField(required=True)
