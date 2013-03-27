# Explore the Microsoft Academic Search API.
# Usage:
# $ python -i acadsearch.py
# 
# >>> q = "information retrieval"
# >>> r = search(q, 1, 10)
# >>> p = get_publications(r)

import json
import requests

f = open("key")
app_id = f.read().strip('\n')
f.close()

def search(query, start, end):
    """Search for a query string using the Academic Search
    API. `start' is the start index (minimum: 1), `end' is the end
    index (minimum: 1).

    At most 100 results can be returned in one search. The result is
    in JSON form."""

    search_url = "http://academic.research.microsoft.com/json.svc/search"

    payload = {}
    payload['AppID'] = app_id
    payload['FullTextQuery'] = query
    payload['StartIdx'] = start
    payload['EndIdx'] = end

    r = requests.get(search_url, params = payload)
    return r

def get_author_names(authors):
    """Given author information from the JSON response, return a list
    of author names."""

    author_names = []
    for author in authors:
        current_name = ''
        current_name += author['FirstName']
        if author['MiddleName'] is not None and len(author['MiddleName']) > 0:
            current_name += ' ' + author['MiddleName']
        if author['LastName'] is not None and len(author['LastName']) > 0:
            current_name += ' ' + author['LastName']

        author_names.append(current_name)

    return author_names

def get_keyword_names(keywords):
    """Given keyword information from the JSON response, return a list
    of keyword names."""

    keyword_names = [keyword['Name'] for keyword in keywords]
    return keyword_names
    
def get_publications(response):
    """Given the response, return the publication information. Also,
    print essential information in an easy-to-read way."""

    j = json.loads(response.text.encode('ascii', 'ignore'))
    publications = j['d']['Publication']['Result']
    print "Number of publications: %d" % (len(publications))

    for pub in publications:
        title = pub['Title']
        year = pub['Year']
        abstract = pub['Abstract']
        authors = pub['Author']
        citations = pub['CitationCount']
        keywords = pub['Keyword']

        author_names = get_author_names(authors)
        keyword_names = get_keyword_names(keywords)

        print
        print "Title: %s (%d)" % (title, year)
        print "Citations: ", citations
        print "Authors: ", author_names
        print "Abstract: ", abstract
        print "Keywords: ", keyword_names
        
    return publications

# Query
q = "information retrieval"
