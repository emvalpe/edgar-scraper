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

import analyze_fillings

final = open("final.json", "r")

last = ""
while True:
	line = final.readline()
	if line == "":break

	last = line
last = json.loads(last)
final.close()

temp = open("processed.json", "r")
total = 0
while True:
	line = temp.readline()
	if not line:break
	else:total+=1
del temp

#cik can be a good way to read until
processed = open("processed.json", "r")

ite = 0
while True:
	line = processed.readline()
	if line == "":break
	ite+=1
	line = json.loads(line)
	if line["cik"] == last["cik"]:
		print(line)
		break

analyze(processed, open("final.json", "a+"), total - ite)