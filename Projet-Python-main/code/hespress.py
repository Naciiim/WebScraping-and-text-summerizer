from bs4 import BeautifulSoup
import requests
import re

def scrape_hes(url):
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}
    page = requests.get(url, headers=HEADERS)

    src = page.content  # variable to store page content
    soup = BeautifulSoup(src, "html.parser")  # beautify code
    # print(soup)
    Matches_Details = []

    # find all divs where exists class...
    article_content = soup.find("div", {'article-content'})

    all_paragraphes = article_content.find_all("p")  # get all a tags
    # matches_number = len(all_matches)
    article_text = ""
    i=0
    for x in all_paragraphes:
        if i==0:
            i=1
            x = x.text.strip()
            article_text = article_text+'\n'+x
            continue
        x = x.text.strip()
        article_text = article_text+'\n'+x
    #suppression espaces vides
    article_text = re.sub(r'\n[\t\n\s]+\n*',r"\n",article_text)
    return article_text.strip()
