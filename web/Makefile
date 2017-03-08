###
### This Makefile is for making the website only!
###

GITHUB_PAGES_BRANCH=gh-pages
THEME = sok

MARKDOWN = python3 -m markdown
BASEDIR = .
DOCSDIR = $(BASEDIR)/content/docs
PAGEDIR = $(BASEDIR)/content/

html:
	hugo --theme=$(THEME)

develop:
	hugo server --theme=$(THEME) --buildDrafts --watch

github: html
	cp -r public/* ../
	git add -A; git commit -m "Rebuilt site" ; git push

.PHONY: html clean develop
