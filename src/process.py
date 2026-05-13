###
### process.py
###

from collections import namedtuple
import time
import re
import csv
import os
import html as html_module

import unicodedata

def normalize_key(text):
    # 1. Decompose characters (e.g., 'é' becomes 'e' + 'accent')
    nfd_form = unicodedata.normalize('NFD', text)
    
    # 2. Filter out the accents (non-spacing marks) and make lowercase
    return "".join(c for c in nfd_form if unicodedata.category(c) != 'Mn').casefold()

def author_key(name):
    """Convert author name (with &nbsp;) to a URL-safe slug."""
    plain = name.replace('&nbsp;', ' ')
    plain = html_module.unescape(plain)
    nfd = unicodedata.normalize('NFD', plain)
    plain = "".join(c for c in nfd if unicodedata.category(c) != 'Mn')
    key = plain.lower().replace(' ', '-')
    key = re.sub(r'[^a-z0-9-]', '', key)
    return key

def author_display(name):
    """Convert author name (with &nbsp;) to a readable display name."""
    return name.replace('&nbsp;', ' ')

def link_authors(authors_str):
    """Wrap each author name in a link to their individual author page."""
    parts = []
    for aname in authors_str.split(', '):
        key = author_key(aname)
        display = author_display(aname)
        parts.append('<a href="/author/' + key + '/">' + display + '</a>')
    return ', '.join(parts)

def last_name(fullname):
    lastspace = fullname.rfind('&nbsp;')
    if lastspace == -1:
        return fullname
    assert lastspace > 1, "Problem with last name: " + fullname
    lastname = fullname[lastspace + 6:]
    # print("lastname: " + lastname)
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
        if not "Title" in paper:
            print("No title for paper: " + str(list(paper.items())))
            continue

        if not paper["Title"]:
            pass
        # print ("Title: " + paper["Title"])
        # print ("URL: " + paper["URL"])
        if paper["URL"]:
            assert ("pdf" in paper["URL"]) or ("https" in paper["URL"]), paper["URL"]
        else:
            print("No URL for paper: " + paper["Title"])
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
            assert (')' not in aname), "Bad name: " + aname
            assert ('and ' not in aname), "Names include and: " + aname
            aname = aname.replace(' ', '&nbsp;')
            nauthors.append(aname)
            if aname in tauthors:
                tauthors[aname].append(paper)
            else:
                tauthors[aname] = [paper]
        paper["Authors"] = ', '.join(nauthors)
    lauthors = list(tauthors.items())
    lauthors.sort(key=lambda a: normalize_key(last_name(a[0])))
    return papers, lauthors, venues

def venue_file(venue):
    if venue == "Oakland":
        return "oakland"
    elif venue == "EuroS&P":
        return "eurosp"
    elif venue == "NDSS":
        return "ndss"
    elif venue == "PETS":
        return "pets"
    elif venue == "SaTML":
        return "satml"
    elif venue == "USENIX":
        return "usenix"
    else:
        assert False, "Bad venue: " + venue
        
def venue_text(venue):
    if venue and venue != "Oakland":
        venuetext = venue
    else:
        venuetext = "S&amp;P"
    return  "<font color='#888'>&nbsp;(" + venuetext + ")</font>" 

def generate_web(title, authors, year, url, venue, showvenue = True):
    if not url:
        urlp = ''
    elif url.startswith("https://"):
        urlp = '<a href="' + url + '">'
    else:
        urlp = '<a href="/papers/' + url + '">'
    return ('<td width="45%" style="padding: 10px; border-bottom: 1px solid #EDA4BD;">' + urlp + '<em>' + title + '</em>' + ('</a>' if url else '') + (venue_text(venue) if showvenue  else "") + '</td><td style="padding: 10px; border-bottom: 1px solid #EDA4BD;">' + authors + "</td>")


def generate_short(title, authors, year, url, venue, papernl=False):
    if not url:
        linked_title = '<em>' + title + '</em>'
    elif url.startswith("https://"):
        linked_title = '<a href="' + url + '"><em>' + title + '</em></a>'
    else:
        linked_title = '<a href="/papers/' + url + '"><em>' + title + '</em></a>'
    
    if papernl:
        return '<p><b>' + linked_title + '</b> &mdash; ' + venue + ' ' + year + '<div class="indented">' + authors + '</div></p>'
    else:
        return linked_title + ' (' + venue + ' ' + year + ')<br><small>' + authors + '</small>'


def generate_author_pages(authors, output_dir):
    """Generate one Hugo content page per author in output_dir."""
    os.makedirs(output_dir, exist_ok=True)
    # Remove stale author pages from previous runs
    for fname in os.listdir(output_dir):
        if fname.endswith('.md'):
            os.remove(os.path.join(output_dir, fname))
    for author_name, papers in authors:
        key = author_key(author_name)
        display = author_display(author_name)
        fpath = os.path.join(output_dir, key + '.md')
        papers_sorted = sorted(papers, key=lambda p: (p["Year"], p["Title"]))
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write('+++\n')
            f.write('title = "' + display + '"\n')
            f.write('+++\n\n')
            # f.write('<center>\n\n')
            # f.write('[SoK Authors](/authors) &middot; [Main Page](/)\n')
            # f.write('</center>\n\n')
            f.write('<h1>' + display + '</h1>\n\n')
            f.write('<p></p>\n')
            for paper in papers_sorted:
                linked = link_authors(paper["Authors"])
                f.write(generate_short(paper["Title"], linked, paper["Year"], paper["URL"], paper["Venue"],papernl=True) + '\n')
            f.write('\n')

if __name__=="__main__":
    papers, authors, venues = read_papers("papers.csv")

    print("Writing byyear.html...")
    with open("byyear.html", "w") as f:
      f.write("""   <table> """)
      lastyear = None
      shading = False
      papers.sort(key = lambda p: (p["Title"]))
      papers.sort(key = lambda p: (p["Year"]), reverse=True)
      for p in papers:
          if not p["Year"] == lastyear:
              lastyear = p["Year"]
              f.write('<tr bgcolor="C46BAE"><td colspan="2" style="bgcolor: #C46BAE; text-align: center; color: #FFFFFF">' + p["Year"] + "</td></tr>")
          row = generate_web(p["Title"], link_authors(p["Authors"]), p["Year"], p["URL"], p["Venue"])
          f.write(("<tr>" if shading else "<tr bgcolor=\"EEEEFE\">") + row + "</tr>")
          shading = not shading
      f.write("""   </table>""") 

    print("Writing by venues...")
    for venue in venues:
        if not venue: continue
        print ("Venue: " + venue)
        fname = venue_file(venue) + ".html"
        with open(fname, "w") as f:
            f.write("""   <table> """)
            lastyear = None
            shading = False
            papers.sort(key = lambda p: (p["Title"]))
            papers.sort(key = lambda p: (p["Year"]), reverse=True)
            for p in papers:
                if not p["Venue"] == venue:
                    continue
                if not p["Year"] == lastyear:
                    lastyear = p["Year"]
                    f.write('<tr bgcolor="C46BAE"><td colspan="2" style="bgcolor: #C46BAE; text-align: center; color: #FFFFFF">' + p["Year"] + "</td></tr>")
                row = generate_web(p["Title"], link_authors(p["Authors"]), p["Year"], p["URL"], p["Venue"], showvenue=False)
                f.write(("<tr>" if shading else "<tr bgcolor=\"EEEEFE\">") + row + "</tr>")
                shading = not shading
            f.write("""   </table>""") 
      
    print("Writing authors.html...")
    with open("authors.html", "w") as f:
      for author in authors:
          key = author_key(author[0])
          display = author_display(author[0])
          # f.write('<b><a href="/author/' + key + '/">' + display + '</a></b><br>')
          f.write('<b>' + display + '</b><br>')
          papers = author[1]
          papers.sort(key = lambda p: p["Year"])
          for paper in papers:
              f.write('<p class="hanging">' + generate_short(paper["Title"], 
                                                            link_authors(paper["Authors"]),
                                                            paper["Year"], paper["URL"], paper["Venue"]) + "</p>")
          f.write("</p><p>")

    print("Writing author pages...")
    author_pages_dir = os.path.join("..", "web", "content", "author")
    generate_author_pages(authors, author_pages_dir)
    print("Wrote " + str(len(authors)) + " author pages to " + author_pages_dir)
