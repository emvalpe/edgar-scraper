import personal_lib

import time as t
import requests

def file_enumerate(cik, output):
    header = personal_lib.random_user_agent("dict")

    url = "https://www.sec.gov/Archives/edgar/data/"+ cik + "/"
    try:
        with requests.get(url, headers=header, timeout=5) as response:
            response = response.text
            response = response[response.find("Directory Listing for /Archives/edgar/data/"):response.find("</table>")]

    except Exception:
        print("failed at: " + cik)
        t.sleep(.5)
        file_enumerate(cik, output)
        return

    links = []
    while True:
        if response.find('href="') == -1:
            break
    
        response = response[response.find('href="'):].replace('href="', "", 1)
        links.append(response[:response.find('"')].replace('"', "", 1))

    files = []
    for i in links:
        i = i.replace("/Archives/edgar/data/", "")
        files.append(i[i.find("/")+1:])
    #file location https://www.sec.gov/Archives/edgar/data/cik/

    output.write(cik + ":" + str(files).replace("[", "").replace("]", "") + "\n")
    print(cik)

def main():
    f = open("ciks.txt", "r")
    ciks = f.readlines()
    enumerated_files = open("enumerated_files.txt", "w+")

    sets = []
    mini = []
    for i in ciks:
        if len(mini) % 10 == 0:
            sets.append(mini)
            mini = []
        mini.append(i.replace("\n", ""))
    sets.append(mini)#to catch the leftover set
    f.close()
    
    for bunch in sets:
        for i in bunch:
            file_enumerate(i, enumerated_files)
            t.sleep(.2)
    
    enumerated_files.close()

main()
