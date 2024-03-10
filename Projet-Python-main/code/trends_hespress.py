from bs4 import BeautifulSoup
import requests
import streamlit as st



def get_trends_image(page):
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}
    page = requests.get(
        page,
        headers=HEADERS)
    src = page.content  # variable to store page content
    soup = BeautifulSoup(src, "html.parser")  # beautify code
    # print(soup)

    image = soup.find("img")  # find all divs where exists class...

   

    image_link=image.get('src')
    return image_link



@st.cache_data(ttl=7200) # cache clears after 7200s
def trends_hespress():
        HEADERS = {
            'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}
        page = requests.get(
            'https://en.hespress.com/',
            headers=HEADERS)
        src = page.content  # variable to store page content
        soup = BeautifulSoup(src, "html.parser")  # beautify code
        # print(soup)

        page = soup.find("div", {'left-side heading-box col'})  # find all divs where exists class...
        all_trends = page.find_all("a", {'wpp-post-title'})  # get all a tags
        article_text = ""
        trends_list=[]
        for x in all_trends:

            trend_link = x.get('href')
            trend_title = x.text
            trend_image=get_trends_image(trend_link)

            subdict={ 'title':trend_title,
                      'image_link':trend_image,
                      'article_link':trend_link}
            trends_list.append(subdict)
        extra_page = soup.find("div", {'group-item col-sm-12 col-md-6 col-xl-4 category-society bloc_col'})
        extra_trend=extra_page.find("div", {'ratio-medium'})
        image = extra_trend.find("img")
        trend_image=image.get('src')
        trend_title=image.get('alt')
        trend_link = extra_page.find_all('a')
        trend_link = trend_link[1].get('href')


        trend_4={ 'title':trend_title,
                      'image_link':trend_image,
                      'article_link':trend_link}
        trends_list.append(trend_4)
        return trends_list




