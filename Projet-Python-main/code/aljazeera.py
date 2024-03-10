import requests
from bs4 import BeautifulSoup
import regex  as  re
import streamlit as st

@st.cache_data(ttl=7200)
def scrape_aljaz(my_url):
    #print(my_url)
    codehtml = requests.get(my_url)
    page_soup = BeautifulSoup(codehtml.content, "html.parser")
    # print("Le code HTML est:",page_soup)
    article = page_soup.find("div", {"class": "wysiwyg wysiwyg--all-content css-ibbk12"})
    try:
        paragraphe = article.find_all("p")
    except AttributeError:
        return 'This is not a valid article, please choose another.'
    fullArticle = ""
    i=0
    for news in paragraphe:
        if i==0: # skip first iteration
            i = 1
            fullArticle = fullArticle + news.text.strip() # no newline before the first paragraph
            continue
        fullArticle = fullArticle + "\n" + news.text.strip()
    
    #suppression des espaces entrelignes
    fullArticle = re.sub(r'\n[\t\n\s]+\n*',r"\n",fullArticle)
    return fullArticle
