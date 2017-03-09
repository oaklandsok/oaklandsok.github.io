###
### process.py
###

from collections import namedtuple
import time
import re
import csv

def read_papers(fname):
    papers = []
    with open(fname, encoding='ISO-8859-1') as csvfile:
        sreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        headers = next(sreader)
        for row in sreader:
           papers.append({key: value for key, value in zip(headers, row)})

    return papers

def generate_web(title, authors, year, url):
    return ("<td style=\"padding: 10px; border-bottom: 1px solid #ddd;\"><a href=\"/papers/" + url + "\"><em>" + title + "</em></td><td style=\"padding: 10px; border-bottom: 1px solid #ddd;\">" + authors + "</td>")

if __name__=="__main__":
    papers = read_papers("papers.csv")

    print ("""   <table> """)
    lastyear = None
    shading = False
    for p in papers:
        if p["Year"] != lastyear:
            lastyear = p["Year"]
            print('<tr bgcolor="CCCC33" color="FFF"><td colspan="2" style="text-align: center; text-color: #FFFFFF">' + p["Year"] + "</td></tr>")
        row = generate_web(p["Title"], p["Authors"], p["Year"], p["URL"])
        print(("<tr>" if shading else "<tr bgcolor=\"EEEECE\">") + row + "</tr>")
        shading = not shading
    print ("""   </table>""") 
