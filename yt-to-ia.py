"""
yt-to-ia.py
Custom script. Upload YouTube videos to the Internet Archive.

Usage: python3 yt-to-ia.py <youtube_URL>

Uploads youtube video to archive.org, along with metadata including creator, date, and description. Leaves a downloaded copy of the video along with a json file of metadata in ./.output/ in the working directory.
"""

import json
import sys
import yt_dlp
from internetarchive import upload

MY_ACCESS_KEY = "v5SsdIdwUq8VAWL5"
MY_SECRET_KEY = "sXvuqvKZH6TvOBmb"
URL = sys.argv[1]

ydl_opts = {'paths': {'home': '.output/'}}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
	info = ydl.extract_info(URL, download=True)
	print("download to local complete: ", info["title"])

with open(".output/" + info["id"] + ".json", "w", encoding="utf-8") as f:
	f.write(json.dumps(ydl.sanitize_info(info)))

filepath = info["requested_downloads"][0]["filepath"]
date = info["upload_date"]
md = {'collection': 'opensource_movies', 'mediatype': 'movies', 'title': info["title"], 'creator': info["uploader"], 'description': URL + "\n\n" + info["description"], 'date': "-".join([date[:4], date[4:6], date[6:8]]), 'subject': info["uploader"]}
print("metadata:", md)

r = upload(info["id"], files=[filepath], metadata=md, access_key=MY_ACCESS_KEY, secret_key=MY_SECRET_KEY)
print("internet archive upload status:", r[0].status_code)
