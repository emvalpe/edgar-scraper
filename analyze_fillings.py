import personal_lib as personal
import requests
from bs4 import BeautifulSoup
import time as t

import json
from pathlib import Path

import spacy

def file_request(url):
	file_str = ''
	try:
		file_str = requests.get(url, headers=headers, timeout=5).text
	except Exception:
		t.sleep(1)
		print("Error getting filling, retrying")
		file_request(url)

	return file_str

def find_aqui(sentence):
	output = 0
	for tokenized_text in range(len(sentence.ents)):
		text = sentence.ents[tokenized_text].text
		if text.find("aqui") != -1:
			output = tokenized_text
			break

	return output

def find_symbols(organization):
	bad_symbols = ["./", "#", "(", ";"]
	loc = 0

	for i in bad_symbols:
		sec = organization.find(i)
		if sec != -1 and loc < sec:
			loc = sec

	return loc

def connect_orgs(sent, loc):#improve
	org = ""
	sentence = sent.text
	chunks = []

	for i in sent.noun_chunks:
		chunks.append(i.text)
	
	for i in sent.ents:#not catching numbers dates/money also require one proper noun
		if sentence.find(i.text) > loc and i.text in chunks and i.label_ == "ORG":
			org = i.text

	tokens = nlp(org.lower())
	bal = False
	for val in tokens:
		if val.tag_ == "NNP":
			bal = True

	if bal == False:#some things will get through, particularly country based statements like "Toronto stock exchange"
		org = ""

	return org

def process_filling(response):
	output = []
	body = BeautifulSoup(response, "xml").get_text()
	if body.find("\n") != -1:
		body = body.replace("\n", " ")

	if body.find("acqui") != -1:
		thingy = len(body)//500000

		for i in range(thingy+1):
			if thingy != 0:
				try:
					doc = nlp(body[i*500000:(i+1)*500000])
				except Exception:
					doc = nlp(body[i*500000:])
			else:
				doc = nlp(body)

			for sentence in doc.sents:

				search = (sentence.text).find("acqui")#expand to merge too
				if search != -1:
					company = connect_orgs(sentence, find_aqui(sentence))

					if company.find(", ") != -1 or company.find("  ") != -1:
						company = company.replace("  ", " ")
						company = company.replace(", ", " ")

					locs = find_symbols(company)

					if locs != 0 and company[:locs].find(" ") == -1:
						company = company[:locs]
					elif locs != 0 and company[:locs].find(" ") != -1:
						company = company[locs:]

					if company not in output and company != "":
						x = True
						for i in output:
							if company.find(i) != -1:#dont add if company in element
								output[output.index(i)] = company
								x = False
								break

						if x == True:
							output.append(company)
	
	return output

def analyze(company):#check filing type
	for i in company["filings"]["recent"]["accessionNumber"]:
		index = company["filings"]["recent"]["accessionNumber"].index(i)#check if form has subsection too, maybe idk
		if company["filings"]["recent"]["form"][index] in forms:

			filing_url = "https://www.sec.gov/Archives/edgar/data/"+company["cik"]+"/"
			fil = i.replace("-", "")
			filing_url += fil + "/" + i + ".txt"
			
			response = file_request(filing_url)
			if response != "":
				owned = process_filling(response)
				if owned != []:
					for o in owned:
						if o not in company["acquired"]:
							company["acquired"].append(i + ":" + o)#write name of aquired company and filing
					
	return company
		
	
headers = personal.random_user_agent("SEC")
forms = ["10-K", "6-K"]#removed 8k and 10q, seems to still catch everything based on current testing

nlp = spacy.load("en_core_web_sm")
p = Path("./").iterdir()
iterat = 0
start = t.time()

print("Starting")
for file in p:
	new_info = []
	if (file.name).find("processed") != -1:
		with file.open() as fr:
			json_dict = json.load(fr)
			
			for i in json_dict:
				if len(i.keys()) > 1:
					i = analyze(i)
					if i["acquired"] != []:
						print("Hits for %s:%s" % (i["name"], str(i["acquired"])))
					new_info.append(i)
				
				iterat += 1
				if(iterat%10000 == 0):
					print("\niteration: " + str(iterat) + " Time(m): " + str((t.time()-start)/60) + "\n")

			fr.close()

		final = open((file.name).replace("processed", "final"), "w+")
		json.dump(new_info, final)
		final.close()

'''
Issues:
 - mentioned some issues in comments
 - utf-8 encoding doesn't work for things like spanish chars, going to have to expand that
'''
