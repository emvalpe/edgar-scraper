# EDGAR-Scraper
This is a set of python scripts designed to scrape the SEC's EDGAR database. While the database itself is a great resource for investors it is much harder to read lots of data. This repo will contain a means of analyzing each filing submitted to the SEC to find any declarations of aquisition. The end goal is to plot out this data to create visualize the American corporate landscape.

Step 1: Download bulk data from the SEC
    https://www.sec.gov/Archives/edgar/daily-index/bulkdata/submissions.zip

Step 2: Extract downloaded file in this project's folder

Step 3: Run extract_data.py to reformat the downloaded data

Step 4: Run analyze_fillings.py, this will analyze all of the fillings extracted by the previous file. This will take multiple hours to complete so keep that in mind.
