"""
yt-to-ia.py
Custom script. Upload YouTube videos to the Internet Archive.

Usage: python3 yt-to-ia.py <youtube_URL> <subject1> <subject2> <etc>

Uploads youtube video to archive.org, along with metadata including creator, date, and description, as well as any subjects entered as args. Leaves a downloaded copy of the video along with a json file of metadata in ./.output/ in the working directory.
"""

import json
import string
import sys
from random import choice
from requests import exceptions
import yt_dlp
from internetarchive import upload

def uploadURL(url):
	MY_ACCESS_KEY = "v5SsdIdwUq8VAWL5"
	MY_SECRET_KEY = "sXvuqvKZH6TvOBmb"
	MAX_RQS = 2

	ydl_opts = {'paths': {'home': '.output/'}}
	with yt_dlp.YoutubeDL(ydl_opts) as ydl:
		info = ydl.extract_info(url, download=True)
		print("download to local complete: ", info["title"])

	with open(".output/" + info["id"] + ".json", "w", encoding="utf-8") as f:
		f.write(json.dumps(ydl.sanitize_info(info)))

	filepath = info["requested_downloads"][0]["filepath"]
	date = info["upload_date"]
	subjects = [info["uploader"], "YouTube"]
	try:
		subjects.extend(sys.argv[2:])
	except IndexError:
		print('no subjects appended. continuing...')
	
	md = {'collection': 'opensource_movies', 'mediatype': 'movies', 'title': info["title"], 'creator': info["uploader"], 'description': url + "\n\n" + info["description"], 'date': "-".join([date[:4], date[4:6], date[6:8]]), 'subject': subjects}
	print("metadata:", md)
	sent = False
	upload_id = info["id"]
	attempts = 0
	while sent == False and attempts < MAX_RQS:
		try:
			print('uploading to', upload_id)
			r = upload(upload_id, files=[filepath], metadata=md, access_key=MY_ACCESS_KEY, secret_key=MY_SECRET_KEY)
			sent = True
			print("internet archive upload status:", r[0].status_code)
		except exceptions.HTTPError as err:
			print("HTTPError raised:")
			print(err.response.status_code)
			print(err.response.text)
			if err.response.status_code == 400:
				if attempts < MAX_RQS:
					upload_id = ''.join(choice(string.digits) for _ in range(4)) + '_' + info["id"]
					print("Retrying with new identifier...")
			elif err.response.status_code == 503:
			#todo: try this only once; separate metadata update to add video description after 200 res
				md.update({'description': url})
				print('md', md)
				if attempts < MAX_RQS:
					print("Retrying without video description...")
			attempts += 1
	
	return 0
	

if __name__ == '__main__':
	url = sys.argv[1]
	uploadURL(url)
	sys.exit(0)
