import re
import wptools
import wikipediaapi

class GenericScrapper:

    def __init__(self):
        self.wiki_wiki = wikipediaapi.Wikipedia('MyProjectName (dhytra97@gmail.com)', 'en')
        self.remove_html = '<[^<]+?>'

    def _print_page_details(self,page):
        print("Page - Title: %s" % page.title)
        print("Page - URL: %s" % page.fullurl)

    def _filter_year(self):
        return
        
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
        # Getting the page
        page = wptools.page(page_title)
        page.get()
        
        released_info = page.data["infobox"]["released"]
        return page, released_info

    def get_page_summary_w_release_date(self, page_title:str, date:str):
        try:
            # Get page details
            page, released_info =  self._getting_page_info()

            if date in released_info:
                print(f" {page_title} :: {released_info} Found ")
                return re.sub("\n", "" ,re.sub(self.remove_html, '', page.data['extract']))
            else:
                print(f" {page_title} :: {released_info} Not Found ")

        except Exception as e:
            print(f" ERROR [get_page_summary_w_release_date] :: {e}")

    def get_plot(self, page_title:str, date:str):
        # Get page details
        page, released_info =  self._getting_page_info()
        return