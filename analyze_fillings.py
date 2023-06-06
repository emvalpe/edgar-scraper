import requests
import urllib3
from bs4 import BeautifulSoup#needs lxml

import personal_lib as personal
import time as t
import random as r
from colorama import Fore#Fore for text coloration, Back for background etc

import json
import os
import spacy

def rainbow(text):
	new_text = ""
	color_list = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.LIGHTRED_EX, Fore.LIGHTGREEN_EX, Fore.LIGHTYELLOW_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTMAGENTA_EX, Fore.LIGHTCYAN_EX]

	for i in text:
		new_text += r.choice(color_list)+i

	return new_text

def file_request(url, to=5):
	file_str = ''
	try:
		file_str = requests.get(url, headers=headers, timeout=to).text
	except requests.ConnectionError:
		t.sleep(1)
		file_request(url)
	except RecursionError:
		t.sleep(100)
		print("Error getting filling max recursion")
		file_request(url)
	except Exception:#supported to catch timeout errors idk why a specific except wont work
		t.sleep(1)
		file_request(url, to=30)

	return file_str

def count_of_keywords(body):
	count = 0
	locs = []
	while True:
		ser = body.find("acqui")
		if ser == -1:
			return count, locs
		else:
			count += 1
			locs.append(ser+5)
			body = body[ser+5:]


def find_symbols(organization):
	bad_symbols = ["./", "#", "(", ";", "  ", ", "]
	loc = 0

	for i in bad_symbols:
		organization.replace(i, "-r-")

	return organization

def connect_orgs(sent, loc):#setup something to state entities and further check the sentence
	org = ""
	sentence = sent.text
	chunks = []
	loc = 0

	for i in sent.noun_chunks:
		if i.text.find("acqui") != -1:
			loc = len(chunks)
		else:
			chunks.append(i.text)
	
	for i in sent.ents:#require one proper noun
		if sentence.find(i.text) > loc and i.text in chunks and i.label_ == "ORG":
			org = i.text
			#print(Fore.LIGHTBLUE_EX+i.text)

	tokens = nlp(org)#issue here with all caps getting through and things with capital non-proper nouns seems that there isn't a very good solution for this as of now
	bal = False
	for val in tokens:
		if val.tag_ == "NNP":
			bal = True
			break
			#lower_version = nlp(val.text.lower()) #attempt to sort previously mentioned issue

	if bal == False:#some things will get through, particularly country based statements like "Toronto stock exchange"
		return ""
	
	#print(Fore.WHITE+org)

	return org

def process_filling(response):
	output = []
	body = BeautifulSoup(response, "xml").get_text()
	length = len(body)

	if body.find("\n") != -1:#problematic if a lot of spaces are removed
		body = body.replace("\n", " ")

	count, locs = count_of_keywords(body)
	if count != 0:
		for i in range(0, length, 500000):
			if len(locs) == 0:
				break
			if i*500000 < locs[0] and (i+1)*500000 > locs[0]:
				rep = []
				for z in range(len(locs)):
					if (i+1)*500000 > locs[0]:
						rep.append(locs[0])#????
						del locs[0]

				try:
					nat = body[i*500000:(i+1)*500000]
					doc = nlp(nat)

				except Exception:
					nat = body[i*500000:]
					doc = nlp(nat)

				for sentence in doc.sents:#could be flawed if a sentence is cut in two

					search = (sentence.text).find("acqui")#expand to "merge" too
					if search != -1 and (sentence.text).find("reacqui"):
						#print(Fore.GREEN+sentence.text)
						company = connect_orgs(sentence, rep[0])#check this function
						del rep[0]
						if company.find(", ") != -1 or company.find("  ") != -1:
							company = company.replace("  ", " ")
							company = company.replace(", ", " ")
						#print(Fore.YELLOW+company)

						comapny = find_symbols(company)#improved block, test

						if company not in output and company != "":
							x = True
							for i in output:
								if company.find(i) != -1 and len(company) > len(i):
									output[output.index(i)] = company
									x = False
									break

							if x == True:
								output.append(company)
	
	return output

def analyze(file, output, total):
	ite = 0
	start = t.time()
	while True:
		line = file.readline()
		if line == "" or line == "\n":continue
		if not line:return
		ite+=1
		company = json.loads(line)
		#print(rainbow(company["name"]))
		if ite%100 == 0:
			end = t.time()
			print(Fore.GREEN+str(ite)+"\\"+str(total)+" with a time(min): "+str((end-start)/60) + " rate of(comapnies/sec): "+str(ite/(end-start)))

		iterat = 0
		for i in company["filings"]["recent"]["accessionNumber"]:
			if company["filings"]["recent"]["form"][iterat] in forms:

				filing_url = "https://www.sec.gov/Archives/edgar/data/"+company["cik"]+"/"
				fil = i.replace("-", "")
				filing_url += fil + "/" + i + ".txt"
				
				response = file_request(filing_url)
				if response != "":
					owned = process_filling(response)
					if owned != []:
						for o in owned:
							if o not in company["acquired"]:
								company["acquired"].append(i + ":" + o)
						
						output.write("\n"+json.dumps(company))
							
			iterat += 1

		if company["acquired"] != []: print(Fore.YELLOW + "Hits for %s:%s" % (company["name"], str(company["acquired"])))	

	output.close()
		
	
headers = personal.random_user_agent("SEC")
forms = ["10-K", "6-K", "8k"]#removed 10q, seems to still catch everything based on current testing

nlp = spacy.load("en_core_web_sm")
iterat = 0
start = t.time()

temp = open("processed.json", "r")
total = 0
while True:
	line = temp.readline()
	if not line:break
	else:total+=1
del temp

print(rainbow("Total Entities: ")+str(total))

file = open("processed.json", "r")

try:
	os.remove(str(file.name).replace("processed", "final"))
except FileNotFoundError:
	pass

analyze(file, open("final.json", "a+"), total)
file.close()
			
os.system("python3 emails.py completed the SEC processing")

'''
Issues:
 - connect_org function has some issues with the ML network being used stated in code also remove SEC things
 - utf-8 encoding doesn't work for things like spanish chars how do I even change this
'''
