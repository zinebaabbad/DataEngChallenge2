from flask_app.routes import articles_routes
from flask_app.data_utils import mongo_setup
import flask

#init flask app
app_ = flask.Flask(__name__)

# registering all routes in the current  flask app
app_.register_blueprint(articles_routes.articles_bp)


if __name__=='__main__':
    #connect to data base
    mongo_setup.connection_init()
    # launch flask on local server
    app_.run(debug=True)
