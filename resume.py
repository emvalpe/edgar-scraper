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
index = 0
while True:
	line = final.readline()
	if line == "":break
	index+=1
	last = line

index = index - 1
last = json.loads(last)#where you left off
final.close()

temp = open("processed.json", "r")
total = 0
while True:
	line = temp.readline()
	if not line:break
	else:total+=1
temp.close()

analyze_fillings.analyze(open("processed.json", "r"), open("final.json", "a+"), total=total, resume=True, prog=index)
os.system("python3 emails.py completed the SEC processing")
