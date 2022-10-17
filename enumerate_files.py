import requests
import personal_lib

def file_enumerate(cik, output):#func to crawl through each link to find files to analyze
    header = personal_lib.random_user_agent("dict")

    url = "https://www.sec.gov/Archives/edgar/data/"+ cik + "/"
    #try:
    response = requests.get(url, headers=header, timeout=5)
    response = response.text[response.text.find("Directory Listing for /Archives/edgar/data/"):response.text.find("</table>")]

    links = []
    while True:
        if response.find('href="') == -1:
            break
    
        response = response[response.find('href="'):].replace('href="', "", 1)
        links.append(response[:response.find('"')].replace('"', "", 1))
    
        req = requests.get("https://www.sec.gov" + links[0], headers = header, timeout=5)
        text = req.text
        text = text[text.find("<table"):text.find("</table>")]

    files = []
    while True:
        if text.find('href="') == -1:
            break

        text = text[text.find('href="'):].replace('href="', "", 1)
        fil = text[:text.find('"')].replace('"', "", 1)
        if fil.find("html") == -1:
            files.append(fil.replace("/Archives/edgar/data/", ""))

    files = files[:-1]#file location https://www.sec.gov/Archives/edgar/data/

    output.write(cik + ":" + str(files).replace("[", "").replace("]", "") + "\n")

def main():# I need to make this run with multiple threads, I will do the same thing as with the CIK-grabber
    f = open("CIKS.txt", "r")
    ciks = f.readlines()
    enumerated_files = open("enumerated_files.txt", "w+")
    for cik in ciks:
        file_enumerate(cik, enumerated_files)

main()
