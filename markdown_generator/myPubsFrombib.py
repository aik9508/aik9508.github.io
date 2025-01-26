#!/usr/bin/env python
# coding: utf-8

# # Publications markdown generator for academicpages
# 
# Takes a set of bibtex of publications and converts them for use with [academicpages.github.io](academicpages.github.io). This is an interactive Jupyter notebook ([see more info here](http://jupyter-notebook-beginner-guide.readthedocs.io/en/latest/what_is_jupyter.html)). 
# 
# The core python code is also in `pubsFromBibs.py`. 
# Run either from the `markdown_generator` folder after replacing updating the publist dictionary with:
# * bib file names
# * specific venue keys based on your bib file preferences
# * any specific pre-text for specific files
# * Collection Name (future feature)
# 

import bibtexparser
import numpy as np
import os

JOU_FMT_STR="""
*  ### J{idx}. [{title}]({doi})
      * {authors}
      * {journal}, {year}.
"""

CON_FMT_STR="""
*  ### C{idx}. [{title}]({doi})
      * {authors}
      * {journal}, {year}.
"""

JOU_CV_FMT_STR="""
*  J{idx}. {authors} "[{title}]({doi})," {journal}, {year}.
"""

CON_CV_FMT_STR="""
*  C{idx}. {authors} "[{title}]({doi})," {journal}, {year}.
"""

HEAD_STR="""---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
---

{% if author.googlescholar %}
  You can also find my articles on <u><a href="{{author.googlescholar}}">my Google Scholar profile</a>.</u>
{% endif %}

{% include base_path %}

<br>



Journal Articles
======
(\* denotes corresponding authors, <sup>+</sup> denotes co-first authors)
"""

CV_HEAD_STR="""
{% include base_path %}

**Journal Articles**

(\* denotes corresponding authors, <sup>+</sup> denotes co-first authors)


"""

MYNAME = 'Ke Wang'

def sort_by_year(x):
    n = len(x)
    years = np.zeros(n)
    for i in range(n):
        entry = x[i]
        years[i] = entry.get('year').value
    idx = np.argsort(years)
    idx = idx[::-1]
    x_sorted = [x[i] for i in idx]
    return x_sorted

def reformat_name(s):
    if ',' in s:
        words = s.split(',')
        last_name = words[0].strip()
        first_name = words[1].strip()
        return f'{first_name} {last_name}'
    else:
        return s

def split_authors(s):
    authors = [x.strip() for x in s.split('and')]
    authors = [reformat_name(x) for x in authors]
    return authors

def add_marks(authors,correspondings,cofirsts,myname=MYNAME):
    marked_authors = []
    for author in authors:
        marked_author = author
        if author == MYNAME:
            marked_author = f'**{marked_author}**'
        if author in correspondings:
            marked_author = f'{marked_author}\*'
        if author in cofirsts:
            marked_author = f'{marked_author}<sup>+</sup>'
        marked_authors.append(marked_author)
    return marked_authors 

def join_authors(authors):
    s = authors[0]
    for i in range(1,len(authors)-1):
        s = s + ', '+ authors[i]
    if len(authors) > 2:
        s = s + ' and ' + authors[-1]
    else:
        s = s + ', and ' + authors[-1]
    return s

def entry_to_md(e,idx,style="pub"):
    doi = e.get('doi').value
    if "http" in doi:
        url = doi
    else:
        url = "https://"+doi
    title = e.get('title').value
    author_str = e.get('author').value
    authors = split_authors(author_str)
    corresponding_authors = []
    cofirst_authors = []
    corresponding_str = e.get('corresponding')
    if not(corresponding_str is None):
        corresponding_str = corresponding_str.value
        corresponding_authors = split_authors(corresponding_str)
    cofirst_str = e.get('cofirst')
    if not(cofirst_str is None):
        cofirst_str = cofirst_str.value
        cofirst_authors = split_authors(cofirst_str)
    marked_authors = add_marks(authors,corresponding_authors,
                               cofirst_authors)
    year = e.get('year').value
    if style == "pub":
        if e.entry_type == 'article':
            journal = e.get('journal').value
            s = JOU_FMT_STR.format(idx=idx,title=title,doi=url,
                                   authors=join_authors(marked_authors),
                                   journal=journal,year=year)
        elif e.entry_type == 'inproceedings':
            journal = e.get('booktitle').value
            s = CON_FMT_STR.format(idx=idx,title=title,doi=url,
                                   authors=join_authors(marked_authors),
                                   journal=journal,year=year)
    elif style == "cv":
        if e.entry_type == 'article':
            journal = e.get('journal').value
            s = JOU_CV_FMT_STR.format(idx=idx,title=title,doi=url,
                                   authors=join_authors(marked_authors),
                                   journal=journal,year=year)
        elif e.entry_type == 'inproceedings':
            journal = e.get('booktitle').value
            s = CON_CV_FMT_STR.format(idx=idx,title=title,doi=url,
                                   authors=join_authors(marked_authors),
                                   journal=journal,year=year)
    else:
        raise ValueError(f"Unrecognized style: {style}")
    return s

if __name__ == '__main__':
    library = bibtexparser.parse_file('mine.bib')
    journal_entries = []
    conference_entries = []
    for i in range(len(library.entries)):
        entry = library.entries[i] 
        if entry.entry_type == 'article':
            journal_entries.append(entry)
        elif entry.entry_type == 'inproceedings':
            conference_entries.append(entry)
    journal_entries = sort_by_year(journal_entries)
    conference_entries = sort_by_year(conference_entries)
    njournal = len(journal_entries)
    nconference = len(conference_entries)
    f = open(os.path.join('..','_pages','publications.md'),'w')
    f.write(HEAD_STR)
    for i,e in enumerate(journal_entries):
        s = entry_to_md(e,njournal-i,style='pub') 
        f.write(s)
        print(s)
    f.write("""
Refereed Conference Proceedings
======
    """)
    for i,e in enumerate(conference_entries):
        s = entry_to_md(e,nconference-i,style='pub')
        f.write(s)
        print(s)
    f.close()

    f = open(os.path.join('..','_includes','publications_cv.md'),'w')
    f.write(CV_HEAD_STR)
    for i,e in enumerate(journal_entries):
        s = entry_to_md(e,njournal-i,style='cv') 
        f.write(s)
        print(s)
    f.write("""
**Refereed Conference Proceedings**


    """)
    for i,e in enumerate(conference_entries):
        s = entry_to_md(e,nconference-i,style='cv')
        f.write(s)
        print(s)
    f.close()

