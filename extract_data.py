import os
import json
from pathlib import Path

#chdir
p = Path("./submission").iterdir()
desired_keys = ["cik", "entityType", "sic", "sicDescription", "name", "tickers", "exchanges", "ein", "description", "category", "stateOfIncorporation", "formerNames", "filings"]

it = 0
info_to_write = []

for file in p:

	if it%99999 == 0 and it != 0:
		file_to_write = open("processed"+str(int(it/99999))+".json","w+")
		json.dump(info_to_write, file_to_write)
		file_to_write.close()

		info_to_write = []

	company = {}

	if file.is_file() == True:
		with file.open() as f:
			try:
				json_read_file = json.load(f)
			except json.decoder.JSONDecodeError:
				print("error")
			
		for key in json_read_file.keys():
			if key in desired_keys:
				company[key] = json_read_file[key]

		company["Aquired"] = []	
		info_to_write.append(company)

		
	it += 1

print("Completed Successfully")
