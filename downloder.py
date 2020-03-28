after_YMD = "1970-01-01"
before_YMD = "2020-03-28"
REQ_SIZE = 1000

# This program retrieve subreddit data within given range.
# The range is not restrictive. For example, you can download monthly or yearly.
import os
import json
import requests
import time
import datetime
import sys
from collections import defaultdict


os.system('pip3 install --user tqdm')

from tqdm import tqdm

# Data Retrieval Example
# r = requests.get("https://api.pushshift.io/reddit/submission/search/?subreddit=legaladvice&after=2019-09-01&before=2019-09-30&size=1")
# data = r.json() # This is a dictionary object
# json_object = json.dumps(data, indent = 4) # This is a json object

# Writing to sample.json 
# with open("2019-09.json", "a+") as outfile: 
#     outfile.write(json_object)

# 1. Convert YYYY-MM-DD to utc
after_utc = datetime.datetime.strptime(after_YMD, '%Y-%m-%d')
after_utc = time.mktime(after_utc.timetuple())
before_utc = datetime.datetime.strptime(before_YMD, '%Y-%m-%d')
before_utc = time.mktime(before_utc.timetuple())
after_utc = int(after_utc)
before_utc = int(before_utc)
print(after_YMD + ':' +  str(after_utc))
print(before_YMD + ':' + str(before_utc))


# 2: Get number of submissions within given range
# https://api.pushshift.io/reddit/submission/search/?subreddit=legaladvice&aggs=subreddit&size=0&after=2018-09-01&before=2018-10-01

nd_url = "https://api.pushshift.io/reddit/submission/search/?subreddit=legaladvice&aggs=subreddit&size=0"


nd_res = requests.get('{}&after={}&before={}'.format(nd_url, after_utc, before_utc))
nd_data = nd_res.json() 
nd_json = json.dumps(nd_data, indent = 4)

#print(nd_json)

numDocs = nd_data['aggs']['subreddit'][0]['doc_count']
print('Number of Documents:',numDocs)

# 3: Retrieve submissions
N = 0
last = ''
ids = []
texts = []
mydict = defaultdict()
url = 'https://api.pushshift.io/reddit/search/submission/?subreddit=legaladvice&fields=id,created_utc,title,selftext'
url = '{}&size={}'.format(url,REQ_SIZE)

cur = after_utc

pbar = tqdm(total=numDocs)

while N < numDocs:
    req = requests.get('{}&after={}&before={}'.format(url,cur,before_utc))
    r_dict = json.loads(str(req.content, "utf-8"))

    mydict.update(r_dict)
#    r_dict = req.json()
    r_json = json.dumps(r_dict, indent = 4, default=lambda o: '<not serializable>')
#    print(r_json)

    i = 0
    for s in r_dict['data']:
        ids.append(s['id'])
        texts.append(s.get('title','') + '\n' +  s.get('selftext',''))
        N += 1
        i += 1

    pbar.update(i)

    cur = int(s['created_utc'])
pbar.close()

print(len(ids))
# print(ids[:10])
# print(texts[:10])
#Writing to sample.json 
json_object = json.dumps(mydict, indent = 4) # This is a json object
filename = '[' + after_YMD + ', ' + before_YMD +')' + ".json" 
with open(filename, "w+") as outfile: 
    outfile.write(json_object)

print("Wrote" + filename)
