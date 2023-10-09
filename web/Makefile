###
### This Makefile is for making the website only!
###

GITHUB_PAGES_BRANCH=gh-pages
THEME = sok

MARKDOWN = python3 -m markdown
BASEDIR = .
DOCSDIR = $(BASEDIR)/content/docs
PAGEDIR = $(BASEDIR)/content/
SRCDIR = $(BASEDIR)/../src/

html:
	cd $(SRCDIR); make
	cat $(SRCDIR)/main.top $(SRCDIR)/byyear.html $(SRCDIR)/main.bottom > $(PAGEDIR)/main.md
	cat $(SRCDIR)/oakland.top $(SRCDIR)/oakland.html $(SRCDIR)/main.bottom > $(PAGEDIR)/oakland.md
	cat $(SRCDIR)/eurosp.top $(SRCDIR)/eurosp.html $(SRCDIR)/main.bottom > $(PAGEDIR)/eurosp.md
	cat $(SRCDIR)/pets.top $(SRCDIR)/pets.html $(SRCDIR)/main.bottom > $(PAGEDIR)/pets.md
	cat $(SRCDIR)/satml.top $(SRCDIR)/satml.html $(SRCDIR)/main.bottom > $(PAGEDIR)/satml.md
	cat $(SRCDIR)/authors.top $(SRCDIR)/authors.html $(SRCDIR)/main.bottom > $(PAGEDIR)/authors.md
	hugo --theme=$(THEME)

develop: html
	hugo server --theme=$(THEME) --buildDrafts --watch

github: html
	cp -r public/* ../
	git add -A; git commit -m "Rebuilt site" ; git push

.PHONY: html clean develop
