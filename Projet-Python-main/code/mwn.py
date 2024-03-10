from bs4 import BeautifulSoup
import requests
import json
import re

def scrape_mwn(url):
    # extraction du code html
    html_content = requests.get(url)
    # parser le code html
    soup = BeautifulSoup(html_content.text, 'html.parser')
    # extaction des paragraphes p l'article
    app_div = soup.find('div', id='app')
    p = app_div.attrs["data-page"]
    p = json.loads(p)  # transformer le contenu en dict json
    p = p["props"]["post"]["post_content"]  # chemin des p de l'article
    # print(json_object) # debug
    # parser l'html du texte pour nettoyage
    main_text_soup = BeautifulSoup(p, 'html.parser')  
    # extraction des tags p
    main_text_soup.find_all('p')

    # suppression du message de copyright
    main_text_soup.find("p", {"class": "article_copyright"}).decompose() 
    
    # suppression du Read also
    for p in main_text_soup.find_all("p"): #on itère sur les paragraphes, on debute par le dernier car 'read also' se trouve en fin de texte
        for link_tag in p.find_all("a"): # on cherche les liens
            joint_list = filter(lambda x: (x != None), [link_tag.find_previous_sibling(string=True) , link_tag.find_previous_sibling("strong")]) # elemnts avant lien + enlever none
            for prev in joint_list: # le read also est tpujours avant le lien, donc on ne cherche que les tags avant 
                if ('read also:' in prev.string.lower()): # verifie si c est le tag voulu
                    p.decompose() # on supprime le tag parent

            

    # suppression des sous titres des paragraphes
    try:
        for sub_title_tag in filter(lambda x: x != None, (main_text_soup.find_all("h3") + main_text_soup.find_all("strong"))): #on cherche les tags strong et h3 et on itère
            if((sub_title_tag.parent.name != "a") & (len(sub_title_tag.findChildren("a")) == 0 )): # pour ne pas supprimer les liens marqués strong
                if(sub_title_tag.parent.name  == "[document]"): # si le tag est au plus haut niveau cad parent = document
                    #print("self")
                    sub_title_tag.decompose() # on détruit le tag
                else:                                              # si le tag est a l'interieur d'un <a>
                    #print("parent decomp")
                    sub_title_tag.parent.decompose() # on détruit le tag parent
    except Exception as e:
        pass
    


    text = main_text_soup.text.strip() # texte

    #suppression de la ville au début
    if(re.search(r"\s-\s",text[:20])): #cherche pour ville dans 20 premiers chars
      city_endpos = re.search(r"\s-\s",text[:20]).end()
      text = text[city_endpos:] # supprimer la ville au début du texte
    
    #suppression des espaces entrelignes
    text = re.sub(r'\n[\t\n\s]+\n*',r"\n",text)
    
    return text
