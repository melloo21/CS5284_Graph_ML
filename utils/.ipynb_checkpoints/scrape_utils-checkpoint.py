import pandas as pd
import requests
import difflib

def split_title_year(df:pd.DataFrame):
    REGEX_Split = r'^(.*)\s\((\d{4})\)$'
    df[['title', 'year']] = df['Title'].str.extract(REGEX_Split)
    return df

def get_scrape_list(df:pd.DataFrame):
    """
    Returns df of titles to scrape split by title and year
    """
    df = split_title_year(df)
    scrape_list = df.groupby(["title"])[["Title"]].count().reset_index()
    return scrape_list.rename(columns={"Title": "unique_counts"})

def get_non_repeat_movie_title(df:pd.DataFrame):
    list_df = get_scrape_list(df)
    return list_df[list_df.Title == 1]

def get_repeat_movie_title(df:pd.DataFrame):
    list_df = get_scrape_list(df)
    return list_df[list_df.Title > 1]


def search_wikipedia(movie_title):
    """
    Search Wikipedia for a movie by title.
    """
    remove_html = '<[^<]+?>'
    search_url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        # "srsearch": f"{movie_title} {release_year} film",  # Include release year and 'film' keyword
        "srsearch" : f"{movie_title}",
        "format": "json",
        "utf8": 1
    }
    
    response = requests.get(search_url, params=params)
    data = response.json()
    # filter results by checking for 'film' in snippet
    data_filtered = get_wiki_title_from_search_results(data, keywords='film')
    if data_filtered is None:
        data = get_wiki_title_from_search_results(data)
    else:
        data = data_filtered
    # Check if results were found
    if data['query']['search']:
        # Return the title of the first relevant result
        # all_titles = [elem["title"] for elem in data['query']['search']]
        first_result_title = data['query']['search'][0]['title']
        return first_result_title
    else:
        return None
        
def get_wiki_title_from_search_results(data, keywords: str=None):
    
    if data['query']['searchinfo']['totalhits'] == 0:
        return None
    if keywords:
        data_filtered = find_word_in_snippets(data, keywords)
        return data_filtered
    else:
        return data


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

def jaccard_similarity(text1, text2):
    # Split the texts into word sets
    set1 = set(text1.lower().split())
    set2 = set(text2.lower().split())

    # Calculate the Jaccard similarity
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    
    return len(intersection) / len(union)
   
def get_most_similar_title(search_txt):
    jacard_score = 0
    final_title = ""
    for elem in search_wikipedia(search_txt):
        if jaccard_similarity(search_txt,elem) > jacard_score:
            jacard_score = jaccard_similarity(search_txt,elem)
            final_title = elem

    return final_title, jacard_score    

def gestalt_pattern_matching(text1, text2):
    '''
    Twice the number of matching (overlapping) characters between the two strings divided by the total number of characters in the two strings.

    Ratcliff/Obershelp string matching formula:     https://en.wikipedia.org/wiki/Gestalt_pattern_matching
    '''
    
    seq = difflib.SequenceMatcher()
    seq.set_seqs(text1.lower(), text2.lower())
    d = seq.ratio()*100
    return d