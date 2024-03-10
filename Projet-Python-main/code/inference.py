import streamlit as st
from transformers import pipeline,BartTokenizerFast
from transformers.pipelines.text2text_generation import SummarizationPipeline
import spacy
from difflib import SequenceMatcher
model_used = 'Yahiael1/mymodel_final_v2'

nlp = spacy.load("en_core_web_sm")

def get_n_first_sent(text, n = 1): # extract first n sentences of text
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents]
    if n == -1: # return all sentences
        return sentences
    return sentences[0:n]

def rem_similiar(text,sum,treshhold = 0.8): # to prevent lead bias
    # uses SequenceMatcher to remove sentences from text that are found in sum
    new_text_list = get_n_first_sent(text,-1)
    if len(new_text_list) > 6:
        k = 6
    else:
        k=3
    list_sent_text = new_text_list[0:k] # to remove similiar phrases from
    new_text_list = new_text_list[k:] # rest of text
    temp = []
    
    list_sent_sum = get_n_first_sent(sum,-1)

    for i, sent_sum in enumerate(list_sent_sum):
        if i == len(list_sent_text):
            break
        for sent_text in list_sent_text: # calcule la similiartité avec ttes les autres phrases
            score_similarité = SequenceMatcher(None, sent_sum, sent_text).ratio()
            if score_similarité >= treshhold:
                temp.append(sent_text)
    return " ".join(temp + new_text_list)

@st.cache(hash_funcs={SummarizationPipeline: lambda _: None})
def load_model():
    return pipeline("summarization", model=model_used)

@st.cache_resource 
def load_tokenizer():
    return BartTokenizerFast.from_pretrained(model_used)

def get_token_len(text):
    tok = load_tokenizer()
    return len(tok("text")["input_ids"])

def summary_wrapper(sum_obj,text,min_len,max_len):
    return sum_obj(text, max_length = max_len,
                             min_length = min_len,
                             #early_stopping = True,
                             clean_up_tokenization_spaces = True,
                             truncation=True, # max token number = 1024
                             num_beams = 6, # nombres de tokens à générer après chaque mot, le modèle ensuite choisit l'un de ces tokens; associée à do_sample
                             do_sample=True, # associée à num_beams, utilise un algorithme non-glouton pour le choix du token suivant
                             repetition_penalty = 1.2, # pénalise les mots redondants en diminuant leur score
                             temperature = 1.2, # modifie hasardément les scores des tokens à choisir pour augmenter ou diminuer la "créativité du modèle" 
                             #num_beam_groups = 4 # doit etre diviseur de num_beams, ajoute un mécanisme promouvant la diversité des tokens générés, ne peut pas etre utlisé avec do_sample
                            )[0]["summary_text"]


def summarize(summarizer_object,desired_length,text):
    n = get_token_len(text)
    #if n < 130:
       # return 'Text is too short, please choose a longer article.'
    if desired_length == 'long':
             max_len = 128
             min_len = 100
    elif desired_length == 'medium':
             max_len = 90
             min_len = 50
    elif desired_length == 'short':
             max_len = 40
             min_len = 10

    first_summary = summary_wrapper(summarizer_object,text,min_len,max_len)
    #return first_summary
    
    new_text =rem_similiar(text,first_summary) # on supprime les phrases extraites
    
    return summary_wrapper(summarizer_object,new_text,min_len,max_len)


