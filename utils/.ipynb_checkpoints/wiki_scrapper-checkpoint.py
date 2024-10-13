import re
import wptools
import wikipediaapi
import sys
import os
from utils.scrape_utils import *

# Suppress output by redirecting sys.stdout temporarily
# Suppress both stdout and stderr by redirecting them to os.devnull
class SuppressOutput:
    def __enter__(self):
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stderr.close()
        sys.stdout = self._original_stdout
        sys.stderr = self._original_stderr

class GenericScrapper:

    def __init__(self):
        self.wiki_wiki = wikipediaapi.Wikipedia('MyProjectName (dhytra97@gmail.com)', 'en')
        self.remove_html = '<[^<]+?>'

    def _print_page_details(self,page):
        print("Page - Title: %s" % page.title)
        print("Page - URL: %s" % page.fullurl)

    def _print_sections(self, sections, level=0):
        for s in sections:
            print("%s: %s" % ("*" * (level + 1), s.title))
            self._print_sections(s.sections, level + 1)

    def _filter_year(self):
        return

    ## Using WikiAPI
    def get_page_sections(self, page_title:str):
        try:
            self._print_sections(self.wiki_wiki.page(page_title).sections)
        except Exception as e:
            print(f" ERROR [get_page_sections] :: {e}")

    def get_section_dict(self, page_title:str):
        try:    
            return {elem.title: elem.text for elem in self.wiki_wiki.page(page_title).sections}
        except Exception as e:
            print(f" ERROR [get_section_dict] :: {e}")

    def get_page_summary(self, page_title:str):
        try:
            if page.exists():
                # Printing page details
                self._print_page_details()
                page = self.wiki_wiki.page(page_title)
                return page.summary        
            else: 
                print("Page does not exist")
        except Exception as e:
            print(f" ERROR [get_page_summary] :: {e}")

    def _getting_page_info(self, page_title:str):
        try:
            with SuppressOutput():
                # Getting the page
                page = wptools.page(page_title)
                page.get()
            
            released_info = page.data["infobox"]["released"]
            return page, released_info
        except Exception as e:
            print(f" ERROR [getting_page_info] :: {e}")

    ## Using WikiMediaAPI (wptools)
    def get_page_summary_w_release_date(self, page_title:str, date:str):
        """
         Returns the release date of movie
         Returns extracted date
        """
        try:
            # Get page details
            page, released_info =  self._getting_page_info(page_title)

            # Format release info
            year_matches = re.search(r'\b(\d{4})\b', released_info)

            if date in released_info:
                print(f" {page_title} {year_matches.group(1)} :: {released_info} Found ")
                return re.sub("\n", "" ,re.sub(self.remove_html, '', page.data['extract']))
            else:
                print(f" {page_title} :: {released_info} Not Found ")

        except Exception as e:
            print(f" ERROR [get_page_summary_w_release_date] :: {e}")