import json
import os
import gzip

def main():
	# extract this file from patch-M
	with open("SoundEntries.json", "r", encoding='utf-8') as f:
		data = json.load(f)


	newdata = {"lookup": [], "data": {}}
	for val in data:
		for idx in range(1,11):
			if val[f"File_{idx}"] and "soundtest" not in val[f"File_{idx}"]:
				t_path = os.path.splitext(val["DirectoryBase"] + "/" + val[f"File_{idx}"])[0]
				head, base = t_path.replace('\\', '/').rsplit("/", 1)
				head = head.lower()
				if head not in newdata["lookup"]:
					id = len(newdata["lookup"])
					newdata["lookup"].append(head)
				else:
					id = newdata["lookup"].index(head)
				if val['ID'] not in newdata["data"]:
					newdata["data"][val['ID']] = []
				newdata["data"][val['ID']].append([id, base])

	with gzip.open('parsed_sounds.json.gz', 'wt', encoding='UTF-8') as ofile:
		json.dump(newdata, ofile)

if __name__ == "__main__":
	main()
