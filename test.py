import requests
import json
import time


access_token_1 = "4765e20eb52046aca325f2c3f895b8a3"
baseurl_1 = "https://api.nytimes.com/svc/search/v2/articlesearch.json"

url_params_1 = {}
url_params_1["api-key"] = access_token_1
url_params_1['begin_date'] = "20160601"
url_params_1['end_date'] = "20161201"

nyt_text = {}

try:
    for i in range(3):
        url_params_1['page'] = i
        r = requests.get(baseurl_1, params = url_params_1)
        time.sleep(1)
        data = json.loads(r.text)
        nyt_text[i] = data['response']['docs']
    cache()
except:
    nyt_text = load()

def cache():
    f = open("testcache.txt", 'w')
    f.write(json.dumps(nyt_text))
    f.close()

def load():
    f1 = open ("testcache.txt",'r')
    cachedic = json.loads(f1.read())
    f1.close()
    return cachedic






# for page in range(3):
#     url_params_1['page'] = page
#     r_1 = requests.get(baseurl_1 ,params=url_params_1)
#     fb_data_1 = json.loads(r_1.text)
#     f_1 = json.dumps(fb_data_1, sort_keys=True, indent=2)
