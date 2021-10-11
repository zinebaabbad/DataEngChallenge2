import bs4 as bs
import urllib.request
from  config.config_parser import *
import dateutil.parser
import dateutil.tz
from flask_app.models.articles import Article

class News_Scraper(object):

    def __init__(self):
        self.news_url = get_config("news_link")["url"]
        # html tags found on the guardian site for articles scraping same for every article page
        self.articles_link_tag= get_config("article_link")
        self.article_body_tag = get_config("article_body")
        self.author_tags_candidates = get_config("author_candidates")
        self.article_date_candidates=get_config("article_date_candidates")


    def init_soup(self,url,parser="html.parser"):
        # connect to link and get html
        source = urllib.request.urlopen(url).read()
        # create soup object wich is a webscraper
        soup = bs.BeautifulSoup(source, features=parser)
        return soup

    def parse_link_list(self,url,tag_value):
        soup=  self.init_soup(url )
        # get list of all articles links in the home page of the guardian
        return set(url.get("href") for url in soup.find_all(tag_value["tag"],tag_value["tag_filter"]))

    def parse_author(self,soupObject):
        '''
        get author info: if author is none usually the guardian didn't mention the author
        exemple1: https://www.theguardian.com/artanddesign/2021/oct/09/bali-without-tourists-once-bustling-hotspots-now-eerie-and-overgrown-a-photo-essay
        '''
        for candidate in self.author_tags_candidates:
            author = soupObject.find(candidate["tag"],candidate["tag_filter"])
            if author is not None :
                if author.get("href") is not None :
                    return {"name":author.text,"profile_link": "https:{}".format(author.get("href"))}
                else:
                    if author.find("a") is not None:
                        return {"name": author.text, "profile_link": "https:{}".format(author.find("a").get("href"))}
                    else :#some authors have a profile link others dont
                        return {"name": author.text}

        return {"name":"Unknown Author"}

    def parse_date(self,soup):

        BST = dateutil.tz.gettz('Europe/London')
        # there is two html tags that can contain a date the date is either stored in div as atext or in a label
        for candidate in self.article_date_candidates:
            date = soup.find(candidate["tag"],candidate["tag_filter"])
            if date is not None:
                if date.find("label") is not None:
                    stringdate=date.find("label").text
                    # the date is expressed in bst time zone we will parse the date and covert it to a datetime
                    return dateutil.parser.parse(stringdate.replace(".", ":"), tzinfos={'BST': BST})

                else:
                    stringdate= date.text
                    # the date is expressed in bst time zone we will parse the date and covert it to a datetime
                    return dateutil.parser.parse(stringdate.replace(".", ":"), tzinfos={'BST': BST})



    def parse_article(self, url):
        '''input url
              # if it's none it means that the url redirects to a video or live video or images album and not an article

        '''
        soup = self.init_soup(url)
        article_content=soup.find(self.article_body_tag["tag"],self.article_body_tag["tag_filter"])
        if article_content is not None:    # if it's none it means that the url redirects to a video or live video or images album and not an article

            article_doc=Article(link=url,
                published_date=self.parse_date(soup),
                author= self.parse_author(soup),
                title=soup.title.text,
                content=article_content.text)
            return article_doc


    def get_all_articles(self):
        '''
        parse all articles in the guarian home page and return a liste of article objects as defined in models
        '''
        article_links=self.parse_link_list(self.news_url,self.articles_link_tag )
        result=list()
        for link in article_links:
            article_doc=self.parse_article(link)
            if article_doc is not None :# this case happens when the link redirect to a page that doesnt contain an article
                result.append(article_doc)

        return result


