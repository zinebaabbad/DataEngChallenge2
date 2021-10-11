import mongoengine
import datetime

class Author(mongoengine.EmbeddedDocument):



    name = mongoengine.StringField(required=True)
    profile_link = mongoengine.URLField()
