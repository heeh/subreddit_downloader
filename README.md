# Subreddit Downloader
* This program downloads /reddit.com/r/legaladvice from 2010 to now.
* The program retrieves "id", "created_utc", "title", and "selftext".
* The downloaded data will be a single json file.
* Execute program with following commands(Takes about 30 minutes)

```bash
$ python3 stream_downloader.py
```
Currently, it downloads submissions from 2010 to 2021.
Set `YEAR_AFTER` and `YEAR_BEFORE` to change the range.
