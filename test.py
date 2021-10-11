
import urllib.request
import json



if __name__=='__main__':


    endpoint = "http://127.0.0.1:5000/api/v1/articles"

    print(urllib.request.urlopen(endpoint + "/keyword/covid").read())
    print(urllib.request.urlopen(endpoint + "/author/guardian").read())
    print(urllib.request.urlopen(endpoint + "/publishdate/2021-10-10T21:00").read())
    print(urllib.request.urlopen(endpoint + "/title/facebook").read())
    print(urllib.request.urlopen(endpoint + "/refresh").read())
    print(urllib.request.urlopen(endpoint).read())