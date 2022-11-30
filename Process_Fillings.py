import requests
import time as t

from personal_lib import *

def caps_check(string):
    for i in string:
        if i.isupper() == True:
            return True
months = ["January", "Febuary", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

class company():
    
    def __init__(self, cik, files, base_link):
        self.cik = cik
        self.files = files
        self.base_link = base_link
                
        self.file_responses = []
        self.filling_types = []
        self.aquired_companies = []
        self.company_information = ""

    #pull filling info
    def file_request(self, file):
        try:
            link_combo = self.base_link+file+"/"
            html = requests.get(link_combo, headers=headers, timeout=5).text
            html = html[:html.find(".txt")]
            html = (html[html.rfind('"'):]+".txt").replace('"', "")

            html = requests.get("https://www.sec.gov"+html, headers=headers, timeout=5).text
            self.file_responses.append(html)
        except:
            t.sleep(.5)
            print("Error getting filling, retrying")
            self.file_request(file)

    #try to pull information about what the company does etc
    def company_info(self):
        filler_info = self.file_responses[0]
        filler_info = filler_info[filler_info.find("FILER:"):filler_info.find("<TYPE>")]

        if filler_info == "":
            try:
                filling = self.file_responses[1]
                filler_info = filling[filling.find("FILER:"):filling.find("<TYPE>")]
            except IndexError:
                print("Error finding a starting form for company: "+self.cik)

        company_name = filler_info[filler_info.find("COMPANY CONFORMED NAME:")+23:].split("\n")
        sic = filler_info[filler_info.find("STANDARD INDUSTRIAL CLASSIFICATION:")+35:].split("\n")
        state_of_operation = filler_info[filler_info.find("STATE:")+7:].split("\n")
        self.company_information = ((cik+",{},{},{}".format(remove_invisible_chars(company_name[0]), remove_invisible_chars(sic[0]), remove_invisible_chars(state_of_operation[0]))).replace(":", ""))
        return self.company_information

    #look for when a filling states they have purchased a company
    def process_filling(self, iter):
        filling = self.file_responses[iter]

        typ = filling.find("TYPE>")
        form_type = filling[typ:].find("<")
        form_type = remove_invisible_chars(filling[typ+5:typ+form_type])
        self.filling_types.append(form_type)

        if form_type in forms:
            body = filling[filling.find("<TEXT>"):filling.find("</TEXT>")]
            search = body.find("acqui")

            if search != -1:
                hit = remove_invisible_chars(body[search:])
                if hit.find(". ") < hit.find(","):#search for clause ends
                    hit = hit[:hit.find(". ")]
                else:
                    hit = hit[:hit.find(",")]

                if hit.find("<") != -1:#html tag removal
                    parts = hit.split("<")
                    hit = ""
                    for i in range(len(parts)):
                        part = parts[i]
                        if part.find(">") == -1:
                            try:
                                if parts[i+1] and parts[i+1].find(">") != -1:
                                    part = ""
                            except:
                                part = part[part.find(">"):]
                        else:
                            part = ""

                        if len(part) != 0:
                            hit += part   

                if hit.find(")") != -1:#removing other noise
                    hit = hit[hit.find(")")+1:]
                elif hit.find("Stock") != -1:
                    hit = hit.replace("Stock", "")
                elif hit.find("'") != -1:
                    hit = hit[hit.find("'")+1:]

                words_salad = hit.split(" ")[1:]
                
                good_salad = ""
                for i in words_salad:#also take into consideration abbreaviations
                    if i.find(";") != -1:
                        i = i[i.find(";")+1:]
                    if i.replace(" ", "") in months:
                        i = ""
                    if i != "" and caps_check(i) == True and i not in good_salad:
                        good_salad += i+" "
                    
                good_salad = good_salad

                if good_salad not in self.aquired_companies and good_salad != "":
                    self.aquired_companies.append(good_salad)
                    #print("Hit!!!! " + good_salad) #because some of these are editted after this function I don't want to output them to the user
        else:
            return

    def conclusion(self, output):
        output.write(self.company_info() + ":Aquired," + str(self.aquired_companies) + ":Fillings," + str(self.filling_types) + ":Links," + str(self.files) + "\n")

        for i in range(len(self.aquired_companies)):
            company = self.aquired_companies[i]
            if company in self.company_information:
                company = ""
            else:
                pass

        print("Finished fillings for: " + self.cik)

f = open("enumerated_files.txt", "r")
lines = f.readlines()

the_big_cheese = {}
for line in lines:
    cik = line[:line.find(":")]
    fillings = []

    line = line[line.find(":"):]
    while True:
        con = line.find(",")
        if con == -1:
            seg = line[line.find("'"):]
            fillings.append(seg.replace("'", "").replace("\n", ""))
            break
        seg = line[line.find("'"):con]
        line = line[con:].replace(",", "", 1)
        fillings.append(seg.replace("'", ""))
    
    the_big_cheese.update({cik:fillings})

f.close()
lines = []

headers = random_user_agent(typ="dict")
ciks = the_big_cheese.keys()
final_stack = open("THE_DB.txt", "w+")

forms = ["10-K", "10-Q", "6-K", "8-K"]
web_chars = ["<", ">"]

for cik in ciks:
    bruh = company(cik, the_big_cheese[cik], ("https://www.sec.gov/Archives/edgar/data/" + cik + "/"))

    for i in range(len(bruh.files)):
        bruh.file_request(bruh.files[i])
        bruh.process_filling(i)

    bruh.conclusion(final_stack)

final_stack.close()

### Got em you thought you had all the companies, nah just the public ones