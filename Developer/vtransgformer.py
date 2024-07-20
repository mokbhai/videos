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

def get_text_from_specific_div(url, div_class):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    divs = soup.find_all('div', class_=div_class)
    text = ' '.join([div.get_text() for div in divs])
    text = text.replace('Thank you so much!', "")
    text = text.replace('Translator: Atlas Studios Editor: Atlas Studios', "")
    text = text.replace('Visit and read more novel to help us update chapter quickly.', "")
    with open('../Text/output.txt', 'a') as f:
        f.write(text)
    return text


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
url = "https://novellive.org/book/80-years-of-signing-in-at-the-cold-palace-i-am-unrivalled/chapter-"
# text = get_all_text_from_website(url)
# text = get_text_from_specific_div(url, "txt")

chapter_index = 221

for i in range(0, 20):
    # print("Getting txt from: ", url + str(i))
    idx = chapter_index + i
    text = get_text_from_specific_div(url + str(idx), "txt")
    while not text:  # Retry the iteration if no text was found
        print("No text found, in " + url + str(idx) + " trying again...")
        text = get_text_from_specific_div(url + str(idx), "txt")
    print(text[:14] + " done\n")

# transformers_translate(text)