import re
import time
# from transformers import MarianMTModel, MarianTokenizer # type: ignore
import requests # type: ignore
from bs4 import BeautifulSoup # type: ignore
from googletrans import Translator # type: ignore
import spacy # type: ignore
import textwrap # type: ignore
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.safari.webdriver import WebDriver # import Safari WebDriver

output_file = '/Users/mokshitjain/Desktop/Audio/Text/output.txt'

def get_html_response(url): 
    return get_html_response_selenium(url, delay=0)
    # return get_html_response_BeautifulSoup(url)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def get_html_response_selenium(url, delay):
    options = Options()
    options.headless = True
    # Load the unpacked extension
    options.add_argument("load-extension=./bExtentions/uBlock0.chromium")  # Adjust the path as necessary

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(delay)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    return soup


def get_html_response_BeautifulSoup(url):
    soup = None

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    while (not soup) or (soup == None):    
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

    return soup

def get_all_text_from_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text()
    with open(output_file, 'a') as f:
            f.write(text)
    return text

def get_text_from_specific_div(soup, div_class=None, div_id=None, translate=0, where='div'):
    
    divs = ""
    if div_class:
        divs = soup.find_all(where, class_=div_class)
    elif div_id:
        divs = soup.find(id=div_id)
    else:
        return None
    
    text = ' '.join([div.get_text() for div in divs])
    text = text.strip()
    
    # if "转码失败,请重试!" in text:
    #     return None
    # if "正在为您转码" in text or "最新网址" in text:
    #     return None
    
    # pattern = r'Chapter \d+ [^\n]*\n'
    # text = re.sub(pattern, '', text)
    # pattern = r'Translator: [^\n]+ Editor: [^\n]+\n?'
    # text = re.sub(pattern, '', text)
    
    # text = text.replace('Translator: Atlas Studios Editor: Atlas Studios', "")
    # text = text.replace('Translator: Nyoi-Bo Studio  Editor: Nyoi-Bo Studio', "")
    # text = text.replace('Visit and read more novel to help us update chapter quickly.', "")
    # text = text.replace("\n\n", " ")
    # text = text.replace("Settings Night Mode :", "")
    # text = text.replace("« PrevNext » ≡ Table of Contents", "")
    # text = text.replace("RAW :", "")
    # text = text.replace("Saving, please wait...", "")
    # text = text.replace("Settings saved..", "")
    # text = text.replace(" Close *You must login to use RAW feature and save the settings permanently.", "")
    # text = text.replace("Font size : \n16", "")
    # text = text.replace("最新网址：www.xiaoshubao.net", " ")
    # text = text.replace("Latest website: www.xiaoshubao.net", " ")
    # text = text.replace("This chapter is not yet finished, click the next page to continue reading", " ")
    # text = text.replace("<-->>", " ")
    text = text.replace("Ads by PubFuture", " ")
    # text = text.replace("br>", " ")
    # text = text.replace("<-->>本章未完，点击下一页继续阅读", " ")
    
    text = text.replace("\n", " ")
    
    # if (translate == 1): 
    #     return google_translate(text)
        
    if text:
        return text
    else:
        return None
    
def get_link_from_id(soup, id_value):
    element = soup.find(id=id_value)
    if element:
        return element.get('href')
    element = soup.find('a', class_=id_value)
    if element:
        return element.get('href')
    else:
        return None
    
def get_link_from_class(soup, class_value):
    element = soup.find('a', class_=class_value)
    
    if element:
        return element.get('href')
    else:
        return None

def transformers_translate(text: str, model_name = "Helsinki-NLP/opus-mt-zh-en"):
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    # Split the text into chunks of 100 characters each
    chunks = textwrap.wrap(text, 100)
    translated_text = ""

    for chunk in chunks:
        inputs = tokenizer(chunk, return_tensors="pt")
        translated = model.generate(**inputs)
        tgt_text = [tokenizer.decode(t, skip_special_tokens=True) for t in translated]
        # Save the translated text
        translated_text += tgt_text[0]

    if translated_text:
            return translated_text
    else:
        return None
        
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
        return translated_text
    else:
        return None

where = 'div'

# Use the function
# url = "https://m-xiaoshubao-net.translate.goog/read/385636/23.html?_x_tr_sl=auto&_x_tr_tl=en&_x_tr_hl=en&_x_tr_pto=wapp" # 320 comp
# base_url = "https://m.xiaoshubao.net"
# text_class = ""
# text_id = "BookText"
# next_class = "pb_next"
# translate = 0
# chapter_index = 52

# url = "https://novellive.org/book/everyone-has-four-skills/chapter-51-chapter-51-the-willing-take-the-bait-1" # 50 chapter are working
# base_url = "https://www.mtlnovel.com/four-skills-for-all/chapter-51-serious-clubs-have-tasks/" # 100 chapter are working
# text_class = "post-content"
# text_id = ""
# next_class = "next"
# translate = 0
# chapter_index = 101

# url = "https://www.uuks5.com/zh_hant/book/804501/436902221.html" # Gao Wu: My cells can evolve indefinitely
# base_url = "https://www.uuks5.com/zh_hant/book/804501/"
# text_class = ""
# text_id = "mlfy_main_text"
# next_class = "nextChapterBottom"
# translate = 0
# chapter_index = 231

# url = "http://www.longmawenxue.com/book/3445/879993.html" # From Little Brat to Supreme Commander: My Unlikely Journey to Leading the Elite Forces
# base_url = "http://www.longmawenxue.com"
# text_class = ""
# text_id = "article"
# next_class = "next_url"
# translate = 0
# chapter_index = 251

# url = "http://www.longmawenxue.com/book/28/62785.html" # code name sura
# base_url = "http://www.longmawenxue.com"
# text_class = ""
# text_id = "article"
# next_class = "next_url"
# translate = 0
# chapter_index = 61

url = "http://www.longmawenxue.com/book/10303/3483982.html" # good-for-nothing young master
base_url = "http://www.longmawenxue.com"
text_class = ""
text_id = "article"
next_class = "next_url"
translate = 0
chapter_index = 333

# url = "https://www.uuks.org/b/192/240161.html" # Temple
# base_url = "https://www.uuks.org"
# text_class = ""
# text_id = "contentbox"
# next_class = "next"
# translate = 0
# chapter_index = 161

# url = "https://www.uuks.org/b/56188/70235161.html" # stepmother
# base_url = "https://www.uuks.org"
# text_class = ""
# text_id = "contentbox"
# next_class = "next"
# translate = 0
# chapter_index = 161

url = "https://novelbjn.novelupdates.net/book/seeking-immortality-in-the-world-of-cultivation/chapter-11" # seeking-immortality-in-the-world-of-cultivation
base_url = "https://novelbjn.novelupdates.net"
text_class = ""
text_id = "chr-content"
next_class = "next_chap"
translate = 0
chapter_index = 11

# url = "https://lightnovel.novelupdates.net/book/heavenly-dao-rankings-i-am-exposed-as-the-sword-god/chapter-512-end-returning-to-the-cultivation-world" # completed
# base_url = "https://lightnovel.novelupdates.net"
# text_class = "chr-c"
# text_id = ""
# next_class = "next_chap"
# translate = 0
# chapter_index = 512

for i in range(0, 300):
    print("Getting Chapter: ", chapter_index + i, " From ",url)

    soup = get_html_response(url)
    
    # with open('../Text/index.html', 'w') as f:
    #     f.write(str(soup))
    
    text = get_text_from_specific_div(soup, div_class=text_class, div_id=text_id, translate=translate, where=where)

    while not text:
        print("No text found, in " + url + " trying again...")
        soup = get_html_response(url)
        text = get_text_from_specific_div(soup, div_class=text_class, div_id=text_id, translate=translate, where=where)
    
    # with open(output_file, 'a') as f:
    #     f.write("\nChapter: " + str(chapter_index + i) + "\n" + text)
    
    with open(output_file, 'a') as f:
        f.write("\n\n" + text)

    next_url = get_link_from_id(soup, next_class)

    while not next_url:
        print("No URL found, in " + url + " trying again...")
        soup = get_html_response(url)
        next_url = get_link_from_id(soup, next_class)
   
    if not next_url.startswith('http'):
        next_url = base_url + next_url

    # url = base_url + str(chapter_index + i)
    url = next_url
 
    print("done\n" + "next -> " + url)

