###
### process.py
###

from collections import namedtuple
import time
import re
import csv

def last_name(fullname):
    lastspace = fullname.rfind('&nbsp;')
    if lastspace == -1:
        return fullname
    assert lastspace > 1
    lastname = fullname[lastspace + 6:]
    print("lastname: " + lastname)
    return lastname

def read_papers(fname):
    papers = []
    venues = []
    tauthors = {}

    with open(fname, encoding='ISO-8859-1') as csvfile:
        sreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        headers = next(sreader)
        for row in sreader:
           papers.append({key: value for key, value in zip(headers, row)})

    # cleanup
    for paper in papers:
        if not paper["Title"]:
            pass
        print ("Title: " + paper["URL"])
        assert ("pdf" in paper["URL"]) or ("https" in paper["URL"])
        authors = paper["Authors"]
        # remove affiliations
        if paper["Venue"] not in venues:
            print ("New venue: " + paper["Venue"])
            venues.append(paper["Venue"])
        nauthors = []
        for author in authors.split(','):
            # print("Author: " + author)
            aname = author.strip()
            affiliation = author.find('(')
            if affiliation > 5:
                aname = author[:affiliation].strip()
            assert (')' not in aname)
            assert ('and ' not in aname)
            aname = aname.replace(' ', '&nbsp;')
            nauthors.append(aname)
            if aname in tauthors:
                tauthors[aname].append(paper)
            else:
                tauthors[aname] = [paper]
        paper["Authors"] = ', '.join(nauthors)
    lauthors = list(tauthors.items())
    lauthors.sort(key = lambda a: last_name(a[0]))
    return papers, lauthors

def venue_text(venue):
    if venue and venue != "Oakland":
        venuetext = "  (" + venue + ")"
    else:
        venuetext = ""
    return venuetext

def generate_web(title, authors, year, url, venue):
    return ('<td width="45%" style="padding: 10px; border-bottom: 1px solid #EDA4BD;"><a href="/papers/' + url + '"><em>' + title + '</em></a>' + venue_text(venue) + '</td><td style="padding: 10px; border-bottom: 1px solid #EDA4BD;">' + authors + "</td>")

def generate_short(title, authors, year, url, venue):
    if url.startswith("https://"):
        return ('<a href=' + url + '><em>' + title + '</em></a> (' + venue + ' ' + year + ')')
    else:
        return ('<a href="/papers/' + url + '"><em>' + title + '</em></a> (' + venue + ' ' + year + ')')

if __name__=="__main__":
    papers, authors = read_papers("papers.csv")

    print("Writing byyear.html...")
    with open("byyear.html", "w") as f:
      f.write("""   <table> """)
      lastyear = None
      shading = False
      papers.sort(key = lambda p: p["Year"], reverse=True)
      for p in papers:
          if not p["Year"] == lastyear:
              lastyear = p["Year"]
              f.write('<tr bgcolor="C46BAE"><td colspan="2" style="bgcolor: #C46BAE; text-align: center; color: #FFFFFF">' + p["Year"] + "</td></tr>")
          row = generate_web(p["Title"], p["Authors"], p["Year"], p["URL"], p["Venue"])
          f.write(("<tr>" if shading else "<tr bgcolor=\"EEEEFE\">") + row + "</tr>")
          shading = not shading
      f.write("""   </table>""") 

    print("Writing authors.html...")
    with open("authors.html", "w") as f:
      for author in authors:
          # print("Author: " + author[0])
          f.write("<b>" + author[0] + "</b><br>")
          papers = author[1]
          papers.sort(key = lambda p: p["Year"])
          for paper in papers:
              # print("Paper: " + str(list(paper.items())))
              f.write('<p class="hanging">' + generate_short(paper["Title"], paper["Authors"], paper["Year"], paper["URL"], paper["Venue"]) + "</p>")
          f.write("</p><p>")
