import os
import json
from pathlib import Path

#chdir
p = Path("./submissions").iterdir()
desired_keys = ["cik", "entityType", "sic", "sicDescription", "name", "tickers", "exchanges", "ein", "description", "category", "stateOfIncorporation", "formerNames", "filings"]

try:
	os.remove("./submissions/placeholder.txt")
	os.remove("processed.json")
except Exception:
	pass

for file in p:

	company = {}
	file_to_write = open("processed"+".json","a+")
	if file.is_file() == True and str(file.name).find("submissions") == -1:
		with open("./submissions/"+file.name, "r") as f:
			while True:
				line = f.readline()
				if not line:break
				try:
					read = json.loads(line)
				except json.decoder.JSONDecodeError:
					print("error at: " + file.name + " probably fine")#fix????
			
		for key in read.keys():
			if key in desired_keys:
				company[key] = read[key]

		if company != {} and company["entityType"].lower() == "operating":
			try:
				excess = company["filings"]["files"]
				if len(excess) != 0:
					for z in excess:
						filee = json.load(open("./submissions/"+z["name"],))
						for kem in company["filings"]["recent"].keys():
							company["filings"]["recent"][kem].append(filee[kem])
					
			except KeyError:
				pass

			company["acquired"] = []	
			file_to_write.write("\n"+json.dumps(company))
		else:continue

file_to_write.close()
print("Completed Successfully")
