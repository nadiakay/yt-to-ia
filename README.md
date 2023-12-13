# yt-to-ia
Custom script. Upload YouTube videos to the Internet Archive.

Usage: python3 yt-to-ia.py <youtube_URL> <subjects ...> [-d DATE] [-c CREATOR] [-a] [-t] [-i]

Options:

-d	--date		Specify a date published other than YouTube upload date. Format <yyyy-mm-dd>
-c	--creator	Specify creator other than YouTube uploader
-a	--audio		Extract and upload audio along with thumbnail; default uploads video
-t	--test		Upload to the test collection for temporary files
-i	--info		Save a json file with YouTube metadata
-h	--help		View help

Uploads youtube video to archive.org, along with metadata from YouTube including creator, date, and description, as well as any subjects specified by the user. Leaves a downloaded copy of the video or audio, optionally along with a json file of YouTube metadata, in .output/ directory within the working directory. On successful upload, displays a 200 status code.
