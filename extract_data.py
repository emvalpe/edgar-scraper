import os
import json
from pathlib import Path

#chdir
p = Path("./submissions").iterdir()
desired_keys = ["cik", "entityType", "sic", "sicDescription", "name", "tickers", "exchanges", "ein", "description", "category", "stateOfIncorporation", "formerNames", "filings"]

try:
	os.remove("processed.json")
except Exception:
	pass

for file in p:

	company = {}
	file_to_write = open("processed"+".json","a+")
	if file.is_file() == True:
		with open("./submissions/"+file.name, "r") as f:
			while True:
				line = f.readline()
				if not line:break
				try:
					read = json.loads(line)
				except json.decoder.JSONDecodeError:
					print("error")
			
		for key in read.keys():
			if key in desired_keys:
				company[key] = read[key]

		if company != {}:
			company["acquired"] = []	
			file_to_write.write("\n"+json.dumps(company))

file_to_write.close()
print("Completed Successfully")
