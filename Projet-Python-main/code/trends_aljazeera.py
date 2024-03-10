from bs4 import BeautifulSoup as soup
import streamlit as st
import re
from scraping_needs import get_content


@st.cache_data(ttl=7800)  # cache clears after 7800s
def trends_aljazeera(user_agent):
    main_url = "https://www.aljazeera.com/"
    contenaire = soup(get_content(main_url, user_agent, 0), "html.parser")

    headers_link = contenaire.find_all("li", {"class": "fte-featured-articles-list__item"})

   

    H3 = []
    for i in headers_link:
        Live=i.find(class_="post-label__text")
        if(Live!=None):
          if(Live.text=="Live updates"):
            continue
        
        
        
        pic = {}
        title = i.find(class_="fte-article__title").find('span').text
        picture = i.find("img")
        image_url = main_url + picture.attrs["src"]
        image_url = re.sub(r"\?(.*)", "", image_url)
        image_url2 = image_url + "?resize=900%2C500%"

        link = i.find("a")
        article_link = main_url + link.attrs["href"]

        pic["title"] = title
        pic["image_link"] = image_url2
        pic["article_link"] = article_link

        H3.append(pic)
    return H3
