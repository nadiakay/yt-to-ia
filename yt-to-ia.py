"""
yt-to-ia.py
Custom script. Upload YouTube videos to the Internet Archive.

Usage: yt-to-ia.py <url> [subjects ...] [-h] [-d DATE] [-c CREATOR] [-a] [-t] [-i]

See -h or --help for options.

Uploads youtube video or audio to archive.org, along with metadata including creator, date, and description, as well as any subjects entered as args. Leaves a downloaded copy of the audio/video (optionally along with a json of metadata) in ./.output/ in the working directory.

Known issues:
-if an audio file is requested after a video from the same url or vice versa, the new file will overwrite the previous
"""

import argparse
import json
import os
import requests
import string
import sys
from random import choice
from requests import exceptions
import yt_dlp
from internetarchive import upload

parser = argparse.ArgumentParser()

parser.add_argument("url", nargs=1, help="youtube url to upload")
parser.add_argument("-d", "--date", help="specify date <yyyy-mm-dd>, other than Youtube upload date")
parser.add_argument("-c", "--creator", help="specify a creator, other than Youtube uploader")
parser.add_argument("-a", "--audio", action="store_true", help="upload audio only (default video)")
parser.add_argument("-t", "--test", action="store_true", help="upload to test_collection")
parser.add_argument("-i", "--saveinfo", action="store_true", help="save a json of youtube metadata")
parser.add_argument("subjects", nargs='*', help="add subjects to internet archive metadata")

args = parser.parse_args()

def fetchMedia(url):
	ydl_opts = {'paths': {'home': '.output/'}}
	collection = 'opensource_movies'
	mediatype = 'movies'
	if args.audio:
		ydl_opts = {'paths': {'home': '.output/'}, 'format': 'bestaudio', 'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}]}
		collection = 'opensource_audio'
		mediatype = 'audio'
	if args.test:
		collection = 'test_collection'
	
	with yt_dlp.YoutubeDL(ydl_opts) as ydl:
		info = ydl.extract_info(url, download=True)
		print("download to local complete: ", info["title"])
	
	if args.saveinfo:	
		with open(".output/" + info["id"] + ".json", "w", encoding="utf-8") as f:
			f.write(json.dumps(ydl.sanitize_info(info)))

	files = [info["requested_downloads"][0]["filepath"]]
	if args.audio:
		thumb = requests.get(info["thumbnail"]).content
		thumbfp = info["id"] + '_' + info['thumbnail'].split('/')[-1].split('?')[0]
		print('thumb', thumbfp)
		with open(".output/" + thumbfp, 'wb') as f:
			f.write(thumb)
			thumbfp = os.path.realpath(f.name)
		files.append(thumbfp)	
	print('files', files)

	subjects = ["YouTube"]
	upload_date = "-".join([info["upload_date"][:4], info["upload_date"][4:6], info["upload_date"][6:8]])
	date = args.date or upload_date
	creator = args.creator or info["uploader"]
	description = "Youtube URL: " + url + "\nUploader: " + info["uploader"] + "\nUpload date: " + upload_date + "\nYouTube description:" + "\n\n" + info["description"]
	if len(args.subjects) > 0:
		subjects.extend(args.subjects)
	md = {'collection': collection, 'mediatype': mediatype, 'title': info["title"], 'creator': creator, 'description': description, 'date': date, 'subject': subjects}
	print("metadata:", md)
	media_info = {'id': info['id'], 'files': files, 'md': md}
	return media_info
	
def uploadMedia(info):
	MY_ACCESS_KEY = "v5SsdIdwUq8VAWL5"
	MY_SECRET_KEY = "sXvuqvKZH6TvOBmb"
	MAX_RQS = 0 #fix
	
	sent = False
	attempts = 0
	while sent == False and attempts < MAX_RQS:
		try:
			print('uploading to', info['id'])
			r = upload(info['id'], files=info['files'], metadata=info['md'], access_key=MY_ACCESS_KEY, secret_key=MY_SECRET_KEY)
			sent = True
			print('internet archive upload status:', r[0].status_code)
		except exceptions.HTTPError as err:
			print('HTTPError raised:')
			print(err.response.status_code)
			print(err.response.text)
			if err.response.status_code == 400:
				if attempts < MAX_RQS:
					info['id'] = ''.join(choice(string.digits) for _ in range(4)) + '_' + info['id']
					print('Retrying with new identifier...')
			elif err.response.status_code == 503:
			#todo: try this only once; update metadata to add video description after getting 200 res
				info['md'].update({'description': url})
				print('metadata:', info['md'])
				if attempts < MAX_RQS:
					print('Retrying without video description...')
			attempts += 1
	
	return 0

if __name__ == '__main__':
	info = fetchMedia(args.url[0])
	uploadMedia(info)
	sys.exit(0)
