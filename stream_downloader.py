OUT_FILE = "outfile.json"
PRETTY_OUT_FILE = "pretty_outfile.json"

YEAR_AFTER = 2010
YEAR_BEFOR = 2021



from reddit_util import YMD2utc, getNumSub

import traceback

REQ_SIZE = 1000

import os
import json
import requests
import time
import datetime
import sys
from collections import defaultdict
from tqdm import tqdm

class StreamArray(list):
    """
    Converts a generator into a list object that can be json serialisable
    while still retaining the iterative nature of a generator.

    IE. It converts it to a list without having to exhaust the generator
    and keep it's contents in memory.
    """
    def __init__(self, generator):
        self.generator = generator
        self._len = 1

    def __iter__(self):
        self._len = 0
        for item in self.generator:
            yield item
            self._len += 1

    def __len__(self):
        """
        Json parser looks for a this method to confirm whether or not it can
        be parsed
        """
        return self._len


#Function that will iteratively generate a large set of data.
def large_list_generator_func(numDocs, after_utc, before_utc):
    global REQ_SIZE
    N = 0
    ids = []
    texts = []
    mydict = defaultdict()

    cur = after_utc
    pbar = tqdm(total=numDocs)
    while N < numDocs:
        url = "https://api.pushshift.io/reddit/search/submission/?subreddit=legaladvice&fields=id,created_utc,title,selftext"
        residue = numDocs - N;
        if residue >= 1000:
            url = "{}&size={}".format(url,REQ_SIZE)
        else:
            url = "{}&size={}".format(url,residue)

        req = requests.get("{}&after={}&before={}".format(url,cur,before_utc))
        print('cur', cur)
        print('before_utc', before_utc)
        try:
            r_dict = json.loads(str(req.content, "utf-8"))
        except Exception:
            traceback.print_exc()

        print(len(r_dict["data"]))
        for doc in r_dict["data"]:
            yield doc
        chunk_size = len(r_dict["data"])
        N += chunk_size
        if chunk_size == 0:
            break
        cur = doc["created_utc"]
        print(cur)
        pbar.update(chunk_size)
    pbar.close()



def stream_write(numDocs: int, after_utc, before_utc):
    #Write the contents to file:
    with open(OUT_FILE, "a") as outfile:
        large_generator_handle = large_list_generator_func(numDocs, after_utc, before_utc)
        stream_array = StreamArray(large_generator_handle)
        for chunk in json.JSONEncoder().iterencode(stream_array):
            if chunk != "[" and chunk != "]":
                outfile.write(chunk)
            #print("Writing chunk: ", chunk)

def main():
    yearDocs = 0
    numDocs = 0
    with open(OUT_FILE, "w") as outfile:
        outfile.write("{ \"data\": [")

    year_list = range(YEAR_AFTER, YEAR_BEFORE)
    for year in tqdm(year_list):
        print(year)
        after_ymd = str(year) + "-01-01"
        before_ymd = str(year+1) + "-01-01"

        after_utc, before_utc = YMD2utc(after_ymd, before_ymd)
        print(after_ymd)
        print(before_ymd)

        print(after_utc)
        print(before_utc)
#        print(after_utc, before_utc)
        yearDocs = getNumSub(after_utc, before_utc)
        print(year, yearDocs)
        stream_write(yearDocs, after_utc, before_utc)
        if year != year_list[-1]:
            with open(OUT_FILE, "a") as outfile:
                outfile.write(", ")
        numDocs += yearDocs
        print(numDocs)

    with open(OUT_FILE, "a") as outfile:
        outfile.write("]}")
    with open(OUT_FILE, "r+") as f:
        data = json.load(f)
        json_object = json.dumps(data, indent=4)
    with open(PRETTY_OUT_FILE, "w") as pf:
        pf.write(json_object)
start_time = time.time()
main()
print("--- %s seconds ---" % (time.time() - start_time))
