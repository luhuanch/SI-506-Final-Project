import unittest
import requests
import json
import string
import time
from pprint import pprint

def rmpunc(s):
    for c in string.punctuation:
        c.replace(c, '')
    return c.lower()

class FBConnection:
    def __init__(self, cache_fname, baseurl, access_token):
        self.url_params = {}
        self.url_params["access_token"] = access_token
        self.url_params["fields"] = "posts.limit(200){message, name, likes.limit(1).summary(1)}"
        self.baseurl = baseurl
        self.cache_fname = cache_fname

    def fb_data(self):
        try:
            res = requests.get(self.baseurl, params= self.url_params)
            fb_data = json.loads(res.text)
            f2 = open(self.cache_fname, 'w')
            f2.write(json.dumps(fb_data))
            f2.close()
            return fb_data
        except:
            return self.load()
    def load(self):
        f3 = open(self.cache_fname, 'r')
        fb_data = json.loads(f3.read())
        return fb_data


class NYTConnection:
    def __init__(self, cache_fname_1, baseurl_1, access_token_1):
        self.url_params_1 = {}
        self.url_params_1["api-key"] = access_token_1
        self.url_params_1['begin_date'] = "20160601"
        self.url_params_1['end_date'] = "20161201"
        self.cache_fname_1 = cache_fname_1
        self.baseurl_1 = baseurl_1

    def fb_data_1(self):
        try:
            nyt_text = {}
            for i in range(3):
                self.url_params_1['page'] = i
                r = requests.get(self.baseurl_1, params = self.url_params_1)
                time.sleep(1)
                data = json.loads(r.text)
                nyt_text[i] = data['response']['docs']
            self.cache(self.cache_fname_1, nyt_text)
            return nyt_text
        except:
            nyt_text = self.load(self.cache_fname_1)
            return nyt_text

    def cache(self, fname, s):
        f = open(fname, 'w')
        f.write(json.dumps(s))
        f.close()

    def load(self, fname):
        f1 = open (fname,'r')
        cachedic = json.loads(f1.read())
        f1.close()
        return cachedic



cache_fname = "cached_results_facebook.txt"
cache_fname_1 = "cached_results_NYT.txt"
access_token = "EAACEdEose0cBAKaVbLV80TGQEhpEp2CUIln2PZBOywsQTXc4M52ZCJLDrGv27RBwV8nwZAXx2vis1BDZByFZCHKaXAigkQYP9biyfVhAunWYuLZB7HUzWCIiTFxtXXt65UKTt2FV6xDBP5aRMtY6psCh5Fq6Lj2rss5ZAWc9fAndAZDZD"
access_token_1 = "4765e20eb52046aca325f2c3f895b8a3"
baseurl = "https://graph.facebook.com/v2.3/5281959998"
baseurl_1 = "https://api.nytimes.com/svc/search/v2/articlesearch.json"

fcon = FBConnection(cache_fname, baseurl, access_token)
nytcon = NYTConnection(cache_fname_1, baseurl_1, access_token_1)

fb_data = fcon.fb_data()
nyt_text = nytcon.fb_data_1()


class Post:
    def __init__(self, postdata): #this one defines the constructors as input.
        if 'name' in postdata:
            self.name = postdata['name']
        else:
            self.name = ""
        if 'message' in postdata:
            self.message = postdata['message']
        else:
            self.message = ""
        if 'id' in postdata:
            self.id = postdata['id']
        else:
            self.id = ""
        if 'total_count' in postdata['likes']['summary']:
            self.total_count = postdata['likes']['summary']['total_count']
        else:
            self.total_count = ""

    def __str__(self):
        return "The top_liked New York Time on facebook is {}.".formart(top_liked[0])

class Post_1:
    def __init__(self, post_1data):#this one defines the constructors as input.
        if 'web_url' in post_1data:
            self.url = post_1data['web_url']
        else:
            self.url= ''
        if 'word_count' in post_1data:
            self.word_count = int(post_1data['word_count'])
        else:
            self.word_count = ''
        if '_id' in post_1data:
            self.id = post_1data['_id']
        else:
            self.id = ''
        if 'snippet' in post_1data:
            self.snippet = post_1data['snippet']
        else:
            self.snippet = ''

    def __str__(self): #this gives the format to show the data i collect from the API.
        return "This artcle's name is {}, and its article message is {}.".format(self.name, self.message)

instancelst = sorted([Post(i) for i in fb_data['posts']['data']], key = lambda x : x.total_count, reverse = True)[:10]

fbmessagelst = [i.message for i in instancelst]

nytinstancelst = []
for i in nyt_text:
    for post in nyt_text[i]:
        nytinstancelst.append(Post_1(post))

nysortedinstancelst = sorted(nytinstancelst, key = lambda x: x.word_count)[:10]

nymessagelst = [i.snippet for i in nysortedinstancelst]


def fbwordcount(fbmessagelst):
    fbwordcount = {}
    for message in fbmessagelst:
        for word in message.split():
            if rmpunc(word) not in fbwordcount:
                fbwordcount[word] = 0
            fbwordcount[word] += 1
    return fbwordcount

def nytwordcount(nymessagelst):
    nytwordcount = {}
    for snippet in nymessagelst:
        for word in snippet.split():
            if rmpunc(word) not in nytwordcount:
                nytwordcount[word] = 0
            nytwordcount[word] += 1
    return nytwordcount


fbwords =  fbwordcount(fbmessagelst)
nytwords =  nytwordcount(nymessagelst)

acc = 0
for key in fbwords:
    if key in nytwords:
        acc +=1
result = float(acc)/10


print "\n---- The Top 10 liked message list of Facebook---- \n "
print fbmessagelst
print "\n---- The top 10 highest word count articles' snippet list of New York Times---- \n"
print nymessagelst
print "\n****On average there are {} dupicated words between Top 10 most liked and highest word count**** \n \n".format(result)


class FinalTest(unittest.TestCase):
    def test_instvar_1(self):
        self.assertEqual(type(nytwords), type({}), "Test type of nytwords")
    def test_instvar_2(self):
        self.assertEqual(type(fbwords), type({}), "Test type of fbwords")
    def test_instvar_3(self):
        self.assertEqual(type(nymessagelst), type([]), "Test type of nymessagelst")
    def test_instvar_4(self):
        self.assertEqual(type(nysortedinstancelst), type([]), "Test type of nysortedinstancelst")
    def test_instvar_5(self):
        self.assertEqual(type(instancelst), type([]), "Test type of instancelst")
    def test_instvar_6(self):
        self.assertEqual(type(fcon), type(nytcon), "Test type of instance")
    def test_instvar_7(self):
        self.assertEqual(type(result), float, "Test type of result")
    def test_instvar_8(self):
        self.assertEqual(type(acc ), int, "Test type of acc")
unittest.main(verbosity=2)
