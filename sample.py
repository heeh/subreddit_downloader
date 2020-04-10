import requests
# Download the number of submissions in a given range
url = "https://api.pushshift.io/reddit/submission/   \
           search/?subreddit=legaladvice&aggs=subreddit& \                                                                               size=0&after=2020-01-01&before=2020-01-31"                                                                         num_subs = requests.get(url)
# Retrieve 1000 submissions with specified fields
url = "https://api.pushshift.io/reddit/search/       \                                                                               submission/?subreddit=legaladvice&            \                                                                               fields=id,created_utc,title,selftext&         \                                                                               size=1000&after=2020-01-01&before=2020-01-31"
subs = requests.get(url)
