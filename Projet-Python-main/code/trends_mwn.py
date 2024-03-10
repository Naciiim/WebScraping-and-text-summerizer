import re
import json
import streamlit as st
from scraping_needs import get_content

@st.cache_data(ttl=7800) # cache clears after 7800s
def trends_mwn(user_agent):
    
    #page uses javascript
    str_main_list = get_content("https://www.moroccoworldnews.com/home/post/zheadlines",user_agent,1) # we want text not html
    
    main_list = json.loads(str_main_list)
    
    
    cards_content = []

    for card in main_list:
        content_dict = {}

        content_dict["image_link"] = card["thumb"]
        content_dict["title"] = card["post_title"]

        try:
            tmp = card["tsize"]
        except KeyError:
            try:
                tmp = card["msize"]
            except KeyError:
                tmp = card["lsize"]
        year = re.search('20\d\d(?=[\\\/])',tmp).group() 
        month = re.search('(?<=[\\\/])\d{1,2}(?=[\\\/])',tmp).group()

        content_dict["article_link"] = "https://www.moroccoworldnews.com/" + str(year) + "/" + str(month) + "/" + str(card["ID"]) + "/" + card["post_name"]
        
        cards_content.append(content_dict)

    return cards_content
