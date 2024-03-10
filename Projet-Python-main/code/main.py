import streamlit as st
st.set_page_config(layout="wide")


from scraping_needs import list_user_agents #list of user agents for scraping
import random
import streamlit.components.v1 as components
from streamlit_image_select import image_select
from main_scraping import main_scrape
from trends_aljazeera import trends_aljazeera
from trends_mwn import trends_mwn
from trends_hespress import trends_hespress
from css import main_css,nav_bar_css,ext_css
from inference import *

# on  charge le modèle
resumeur = load_model()

mwn_trends = trends_mwn(list_user_agents[19])[0:6]
hes_tends = trends_hespress()
aljaz_tends = trends_aljazeera(list_user_agents[11])[0:6]

image_list=[]
caption_list=[]

def get_link_from_image(image_link):
    for i in mwn_trends + hes_tends + aljaz_tends:
        if image_link == i["image_link"]:
            return i["article_link"]

def link_to_text(user_input):
  return main_scrape(user_input)


st.markdown(ext_css,unsafe_allow_html=True)
st.markdown(main_css,unsafe_allow_html=True)
st.markdown(nav_bar_css,unsafe_allow_html=True)


with st.expander(r":balloon: ${\huge \text{Quick grab}}$",expanded = 0):
  option_site = st.selectbox("Choose a news outlet", options=("Morocco World News", "Hespress","Aljazeera"))

  if option_site=="Morocco World News":
    for i in range(len(mwn_trends)):
      image_list.append(mwn_trends[i]["image_link"])
      caption_list.append(mwn_trends[i]["title"])
  elif option_site=="Hespress":
    for i in range(len(hes_tends)):
      image_list.append(hes_tends[i]["image_link"])
      caption_list.append(hes_tends[i]["title"])
  elif option_site=="Aljazeera":
    for i in range(5):
      image_list.append(aljaz_tends[i]["image_link"])
      caption_list.append(aljaz_tends[i]["title"])


  img = image_select(
      label="Choose an article to summarize: ",
      images=image_list,
      captions=caption_list,
      #use_container_width=False
  )

  sum_from_img = st.button("Get text of article!")


col1,col2,col3,col3_5,col4,col5 = st.columns([1.5,0.2,1,0.2,0.75,0.8]) # dont change these values cuz they work on compact mode

with col1:
  st.markdown("<br>",unsafe_allow_html=True)
  option = st.selectbox("Choose your input option", options=("Text", "Link"),help="""
For link inputs, you can choose any article from these 3 websites:
* [Morocco World News](https://www.moroccoworldnews.com/)
* [Hespress english](https://en.hespress.com/)
* [Aljazeera english](https://www.aljazeera.com/)
    """
    )



with col3:
   #summary_length = st.radio("Desired summary length:",
    #                        ["short", "medium", "long"])
   summary_length= st.select_slider(
    'Desired summary length:',
    options=['short', 'medium', 'long'])

with col4:
  st.markdown("<br>",unsafe_allow_html=True)
  sum_button = st.button("Summarize")



flag = 1
if sum_from_img:
  chosen_link = str(get_link_from_image(img))
  option = "Text"
  text_from_link=st.text_area("Your article's text : ", value=main_scrape(chosen_link))
  st.session_state.user_text = text_from_link
  flag = 0


if flag:
  if (option == "Text"): #to make sure lines 118 and 110 are not both executed(if user chose image, we shouldnt add another text area)
    if 'user_text' in st.session_state:
      text_from_link = st.text_area("Put the text of the article here",value=st.session_state.user_text)
    else:
      text_from_link = st.text_area("Put the text of the article here")
  elif option == "Link": 
      user_input_link = st.text_input("Paste your link here")



if(sum_button):  # user clicked summarize
  if (flag == 0): # article text area already generated
      st.divider()

  else: # no text area created yet
    if (option == "Link") :
      text_from_link=st.text_area("Your article's text : ", value=link_to_text(user_input_link))
        
      #summary = summarizer(text_from_link, max_length=100, min_length=30, do_sample=False)
        
      #st.write(summary[0]['summary_text'])
  summary = st.text_area('Article summary:', value=summarize(resumeur,summary_length,text_from_link), disabled=True)
  
