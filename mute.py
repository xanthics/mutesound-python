#
# Simple program to generate a sequence of silent files based on a supplied list
# This script requires ffmpeg to be available
#

import pathlib
import os
import json
from pydub import AudioSegment

import gzip
import shutil

TEMP_SOUND_LOOKUP = 'lookup_sb_zan.json'

def setup(sbarchive):
	# remove any existing sound blanking
	if pathlib.Path('sound').is_dir():
		for result in os.listdir("sound"):
			tpath = os.path.join("sound", result)
			if pathlib.Path(tpath).is_file():
				os.remove(tpath)
			else:
				shutil.rmtree(tpath)

	# decompress and return our lookup table
	with gzip.open('parsed_sounds.json.gz', 'rt', encoding='UTF-8') as data:
		return json.load(data)

def main(lookup):
	with open("sounds.txt", "r") as f:
		# allow user to add comments to lines in sounds.txt with `,`
		sounds = [x.split(",", 1)[0].strip() for x in f.readlines()]

	for c, snd in enumerate(sounds, start=1):
		print(f"Handling: {snd} ({c} of {len(sounds)})")
		for obj in lookup['data'][snd]:
			print(f"creating {lookup['lookup'][obj[0]]}/{obj[1]}")
			outpath = os.path.join(lookup['lookup'][obj[0]], obj[1])
			outfile = pathlib.Path(outpath)
			outfile.parent.mkdir(exist_ok=True, parents=True)
			song = AudioSegment.silent(duration=0)
			song.export(outpath + ".wav", format="wav")
			with open(outpath + ".ogg", 'w') as _:
				pass
	return

if __name__ == '__main__':
	if pathlib.Path('parsed_sounds.json.gz').is_file() and pathlib.Path("sounds.txt").is_file():
		lookup = setup('parsed_sounds.gz')
		main(lookup)
	else:
		print("'sounds.txt' or 'parsed_sounds.json.gz not found, exiting.")
		exit()
