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

    # cleanup
    for paper in papers:
        if not paper["Title"]:
            papers.delete(paper)
        print ("Title: " + paper["Title"])
        assert "pdf" in paper["URL"]
        authors = paper["Authors"]
        # remove affiliations
        nauthors = []
        for author in authors.split(','):
            aname = author.strip()
            affiliation = author.find('(')
            if affiliation > 5:
                aname = author[:affiliation].strip()
            assert (')' not in aname)
            assert ('and ' not in aname)
            nauthors.append(aname)
        paper["Authors"] = ', '.join(nauthors)
    return papers

def generate_web(title, authors, year, url):
    return ('<td width="45%" style="padding: 10px; border-bottom: 1px solid #ddd;"><a href="/papers/" + url + "\"><em>' + title + '</em></td><td style="padding: 10px; border-bottom: 1px solid #ddd;">' + authors + "</td>")

if __name__=="__main__":
    papers = read_papers("papers.csv")

    print ("""   <table> """)
    lastyear = None
    shading = False
    for p in papers:
        if not p["Year"] == lastyear:
            lastyear = p["Year"]
            print('<tr bgcolor="CCCC33"><td colspan="2" style="bgcolor: #CCCC33; text-align: center; color: #FFFFFF">' + p["Year"] + "</td></tr>")
        row = generate_web(p["Title"], p["Authors"], p["Year"], p["URL"])
        print(("<tr>" if shading else "<tr bgcolor=\"EEEECE\">") + row + "</tr>")
        shading = not shading
    print ("""   </table>""") 
