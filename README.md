# EDGAR-Scraper
This is a set of python scripts designed to the SEC's EDGAR database. While the database itself is a great resource for investors it is much harder to lots of data collection and plotting. This repo will contain a set of step to enumerate the CIKs of every public company in America, find all of the fillings made to the SEC, and lastly look to find which companies are own by other companies. I was interested in exploring this question as well as practicing my usage of python to map the EDGAR database as quickly as possible.

Notes:
The Sec has a maximum request per second amount of 10, what are we in the 90's?????

Step 1: CIK_enumerator.py
 - this will find all of the ciks currently in the EDGAR DB.

Step 2: enumerate_files.py
 - utilizing the file generated by the previous script, this will pull all of the links for each filling based on the cik
 - also takes a little longer to run

Step 3: Process_Fillings.py 
 - this will take the longest to run, like a few days, it doesn't matter how fast your connection is
 - this analyzes all of the links generated by the last file
 - it will output a db of all the public companies working in America and any of the public or private companies they own
