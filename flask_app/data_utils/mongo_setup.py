from mongoengine import connect
from  config.config_parser import *

import certifi

def connection_init():
    db_uri = get_config("database")["db_uri"]
    ca = certifi.where()
    connect(host=db_uri,tlsCAFile=ca)

