import requests

def get_search_results_from_movie_title(movie_title): 
    S = requests.Session()

    URL = "https://en.wikipedia.org/w/api.php"

    # add 'film' at the end to make results more relevant
    SEARCHPAGE = movie_title + ' film'
    PARAMS = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": SEARCHPAGE
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()

    return DATA

def get_wiki_title_from_search_results(data, keywords: str=None):
    if data['query']['searchinfo']['totalhits'] == 0:
        return None
    if keywords:
        data_filtered = find_word_in_snippets(data, keywords)
        return data_filtered['query']['search']
    else:
        return data['query']['search']


# Function to check for the word "film" in the snippets
def find_word_in_snippets(data, word):
    results = dict()
    results['query'] = dict()
    results['query']['search'] = []
    for entry in data['query']['search']:
        snippet = entry['snippet']
        if word in snippet:
            results['query']['search'].append(entry)
    
    return results


def fetch_wiki_data(wiki_title: str):
    params = {
        'action': 'parse',
        'page': wiki_title,
        'prop': 'wikitext',   
        'format': 'json'
    }

    r = requests.get("https://en.wikipedia.org/w/api.php", params=params)
    data = r.json()