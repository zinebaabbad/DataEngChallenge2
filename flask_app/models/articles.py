import datetime
import mongoengine

from flask_app.models.authors import Author


class Article(mongoengine.Document):

    registered_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    title = mongoengine.StringField(required=True,unique=True)
    content = mongoengine.StringField(required=True)
    link = mongoengine.URLField()
    published_date = mongoengine.DateTimeField()


    author = mongoengine.EmbeddedDocumentField(Author)

'''
    meta = {
        'db '=' 'test',
             username = 'user',
                        password = '12345',
                                   host = 'mongodb://admin:qwerty@localhost/production'
        'db_alias': 'ArticlesDB',
        'collection': 'Article'
    }'''
