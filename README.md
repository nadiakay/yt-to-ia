# yt-to-ia
Custom script. Upload YouTube videos to the Internet Archive.

Usage: python3 yt-to-ia.py <youtube_URL>

Uploads youtube video to archive.org, along with metadata including creator, date, and description. Leaves a downloaded copy of the video along with a json file of metadata in .output/ folder in the working directory.

On successful upload you will see a 200 status code.

Known issues:
- Some videos will be flagged as spam depending on the metadata, likely due to the contents of the video description. An error message will let you know when this happens.
