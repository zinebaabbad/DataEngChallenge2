

from flask import  request
from flask_app.models.articles import Article
import json
import dateutil.parser
import re

from flask_app.data_utils import tf_idf_search, news_scraper as ns



#ftech all articles in database
def fetch_all_article():

    try:
        return Article.objects.all().to_json()
    except Exception as e:
        # Error while trying articles
        return str(e), 404
#fetch  articles by criterea published date greater than given date , by author name ,by title
def fetch_article_from_date(timestamp):
    try:
        try:
            dateutil.parser.parse(timestamp)
        except Exception as e :
            return "Incorrect date format : "+str(e), 400
        return Article.objects.filter(published_date__gte=dateutil.parser.parse(timestamp)).to_json()
    except Exception as e:
        # Error while trying to fetch author
        return str(e), 404
def fetch_article_author_like(authorname):
    try:
        return Article.objects.filter(author__name=re.compile('.*'+authorname+'.*', re.IGNORECASE)).to_json()
    except Exception as e:
        # Error while trying to fetch author
        return str(e), 404

def fetch_article_title_like(title):
    try:
        return Article.objects.filter(title=re.compile('.*'+title+'.*', re.IGNORECASE)).to_json()
    except Exception as e:
        # Error while trying to fetch article
        return str(e), 404

def refresh_database():
    try:
        # scrap articles in order to get recently published articles 
        scraper=ns.News_Scraper()
        all_articles=scraper.get_all_articles()
        list_res=list()
        # add the scraped articles to the data base if it already exist a failed status will be sent 
        for article_doc in all_articles :
            try :
                list_res.append({"status":"success","article":article_doc.save().to_json()})
            except Exception as e:
                list_res.append({"status": "failed"+str(e), "article": article_doc.to_json()})

        return json.dumps(list_res),200
    except Exception as e:
        # Error while trying to refresh  the database
        return str(e), 404

def fetch_article_by_keyword(query):
    try:
        all_articles=Article.objects.all()
        # only extract content in order to form the corpus a collection of documents for tf idf algorthm
        corpus=[article.content for article in all_articles ]
        # get index of articles containns keyword
        index_list=tf_idf_search.get_similarity(query, corpus)
        result_articles=list()
        for i in index_list:
            #based on the index return the similar articles full json
            result_articles.append(list(all_articles)[i].to_json())
        return json.dumps(result_articles) ,200
    except Exception as e:
        # Error while trying to refresh  the database
        return "init", 404

