from transformers import MarianMTModel, MarianTokenizer # type: ignore
import requests # type: ignore
from bs4 import BeautifulSoup # type: ignore
from googletrans import Translator # type: ignore
import spacy # type: ignore
import textwrap # type: ignore

def get_all_text_from_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text()
    with open('../Text/output.txt', 'a') as f:
            f.write(text)
    return text

def get_html_responce(url):
    soup = None

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    while (not soup) or (soup == None):    
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

    return soup

def get_text_from_specific_div(soup, div_class):

    divs = soup.find_all('div', class_=div_class)
    text = ' '.join([div.get_text() for div in divs])

    text = text.replace('Thank you so much!', "")
    text = text.replace('Translator: Atlas Studios Editor: Atlas Studios', "")
    text = text.replace('Visit and read more novel to help us update chapter quickly.', "")

    with open('../Text/output.txt', 'a') as f:
        f.write(text)

    if text:
        return text
    else:
        return None
    
def get_link_from_id(soup, id_value):
    element = soup.find(id=id_value)
    
    if element:
        return element.get('href')
    else:
        return None

def transformers_translate(text: str, model_name = "Helsinki-NLP/opus-mt-zh-en"):
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    # Split the text into chunks of 100 characters each
    chunks = textwrap.wrap(text, 100)

    for chunk in chunks:
        inputs = tokenizer(chunk, return_tensors="pt")
        translated = model.generate(**inputs)
        tgt_text = [tokenizer.decode(t, skip_special_tokens=True) for t in translated]
        # Save the translated text
        with open('transformers_text.txt', 'a') as f:
            f.write(tgt_text[0])

def spacy_translate(text: str, model_name = "zh_core_web_sm"): 
    # Load the spacy model for Chinese to English translation
    nlp = spacy.load(model_name)

    # Translate the text
    doc = nlp(text)
    # print([(w.text, w.pos_) for w in doc])

    translation = doc.translate(to_lang="en")

    print(translation)

def google_translate(text):
    translator = Translator(service_urls=['translate.google.com'])
    translated = translator.translate(text, dest='en')
    if translated and translated.text:
        translated_text = translated.text
        with open('google_text.txt', 'a') as f:
            f.write(translated_text)
    else:
        print("Translation failed. Please try again.")

# Use the function
url = "https://novellive.org/book/80-years-of-signing-in-at-the-cold-palace-i-am-unrivalled/chapter-221" # 260 comp
chapter_index = 221

# url = "https://novellive.org/book/everyone-has-four-skills/chapter-" # 100 chapter are working
# chapter_index = 101

for i in range(0, 20):
    print("Getting Chapter: ", chapter_index + i, " From ",url)

    soup = get_html_responce(url)

    text = get_text_from_specific_div(soup, "txt")

    while not text:
        print("No text found, in " + url + " trying again...")
        soup = get_html_responce(url)
        text = get_text_from_specific_div(soup, "txt")

    next_url = get_link_from_id(soup, "next")

    while not next_url:
        print("No URL found, in " + url + " trying again...")
        soup = get_html_responce(url)
        next_url = get_link_from_id(soup, "next")

    url = next_url

    print("done\n")

# transformers_translate(text)