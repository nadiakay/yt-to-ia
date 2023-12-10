"""
ia-metadata.py

usage: python3 ia-metadata.py <subject> ...

used to append subjects to an internet archive item
"""

import sys
from internetarchive import get_item, modify_metadata

def appendSubjects(id, inputs):
	item = get_item(id)
	subjects = item.metadata['subject']
	if isinstance(subjects , str):
		subjects = [subjects]
	subjects.extend(inputs)
	r = modify_metadata(id, metadata={'subject': subjects})
	print("status:", r)
	
if __name__ == '__main__':
	appendSubjects(sys.argv[1], sys.argv[2:])
	sys.exit(0)
