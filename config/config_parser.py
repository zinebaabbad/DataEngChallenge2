import configparser
from pathlib import Path
import yaml

def get_config(section,file_path=None):

    if file_path is None:
        #find config.yaml path its in the same folder
        file_path = Path(__file__).with_name('config.yaml')
    # open file and load config in a dictionnary form
    stream=open(file_path, 'r')
    config = yaml.safe_load(stream)

    try :
        return config[section]
    except :
        return None
