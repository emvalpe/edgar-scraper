# EDGAR-Scraper:
This is a set of python scripts designed to scrape the SEC's EDGAR database. While the database itself is a great resource for investors it is much harder to read lots of data. This repo will contain a means of analyzing each filing submitted to the SEC to find any declarations of aquisition. The end goal is to plot out this data to create visualize the American corporate landscape.

Step 1: Download bulk data from the SEC
    https://www.sec.gov/Archives/edgar/daily-index/bulkdata/submissions.zip
    run: "python -m spacy download en_core_web_sm" in the mean time.
   
Step 2: run "pip install -r requirements.txt" in the directory you installed this in, while you wait

Step 3: Extract downloaded file in this project's folder
- mkdir /submissions && unzip submissions.zip -d /submissions

Step 4: Run extract_data.py to reformat the downloaded data

Step 5: Run start.py, this will analyze all of the fillings extracted by the previous file. This will take multiple days(42 is my current estimate) to complete so keep that in mind.
 - If you ever stop the execution of this run resume.py to continue execution

#List of Improvements to make:
 - there are some filter issues I can't seem to fix
 - CUDA errors with the ml too
 - https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent
