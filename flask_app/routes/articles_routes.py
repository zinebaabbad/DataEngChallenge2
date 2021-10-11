from flask import Blueprint
from flask_app.controllers.articles_controller import *
articles_bp = Blueprint('articles_controller', __name__)



articles_bp.route("/api/v1/articles", methods=['GET'])(fetch_all_article)
articles_bp.route("/api/v1/articles/author/<authorname>", methods=['GET'])(fetch_article_author_like)
articles_bp.route("/api/v1/articles/publishdate/<timestamp>", methods=['GET'])(fetch_article_from_date)
articles_bp.route("/api/v1/articles/title/<title>", methods=['GET'])(fetch_article_title_like)
articles_bp.route("/api/v1/articles/refresh", methods=['GET'])(refresh_database)
articles_bp.route("/api/v1/articles/keyword/<query>", methods=['GET'])(fetch_article_by_keyword)

