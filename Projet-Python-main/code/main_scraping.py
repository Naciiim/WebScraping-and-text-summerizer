from urllib.parse import urlparse
from hespress import scrape_hes
from aljazeera import scrape_aljaz
from mwn import scrape_mwn
import streamlit as st
import validators

@st.cache_data
def main_scrape(url):
    if not validators.url(url):
        return "We're sorry, but the link you provided seems to be invalid. Please double-check that the URL is correct and properly formatted."
    
    domain = urlparse(url).netloc
    if "moroccoworldnews.com" in domain:
        return scrape_mwn(url)
    if "en.hespress.com" in domain:
        return scrape_hes(url)
    if "aljazeera.com" in domain:
        return scrape_aljaz(url)
    else:
        return "We're sorry, this website is not currently supported. To see a list of supported websites, click the '?' next to the input option."
