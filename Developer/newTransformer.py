from transformers import MarianMTModel, MarianTokenizer
import requests
from bs4 import BeautifulSoup
from googletrans import Translator
import spacy
import textwrap
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

output_file = '../Text/output.txt'

def get_html_response(url): 
    return get_html_response_selenium(url, delay=5)

def get_html_response_selenium(url, delay):
    options = Options()
    options.headless = False  # Set to True for headless mode, but context menu might not work
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get(url)
        time.sleep(delay)  # Wait for the page to load

        # Simulate right-click on the page
        action = ActionChains(driver)
        action.context_click().perform()
        
        # Wait for the translation to complete
        time.sleep(delay)
        
        # Get the translated page source
        soup = BeautifulSoup(driver.page_source, 'html.parser')
    except Exception as e:
        print(f"An error occurred: {e}")
        soup = None
    finally:
        driver.quit()
    
    return soup

def get_html_response_BeautifulSoup(url):
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

def get_text_from_specific_div(soup, div_class=None, div_id=None, translate=0):
    if not soup:
        return None
    
    divs = []
    if div_class:
        divs = soup.find_all('div', class_=div_class)
    elif div_id:
        divs = soup.find_all('div', id=div_id)
    else:
        return None

    text = ' '.join([div.get_text() for div in divs])
    text = text.strip()
    text = text.replace("\n", " ")
    text = text.replace("  ", " ")
    # Filtering out unwanted text
    filters = [
        "转码失败,请重试!", "正在为您转码", "最新网址", "Translator: Atlas Studios", 
        "Editor: Atlas Studios", "Visit and read more novel to help us update chapter quickly.",
        "\n\n", "Settings Night Mode :", "« PrevNext » ≡ Table of Contents", "RAW :",
        "Saving, please wait...", "Settings saved..", " Close *You must login to use RAW feature and save the settings permanently.",
        "Font size : \n16", "Latest website: www.xiaoshubao.net", "This chapter is not yet finished, click the next page to continue reading",
        "<-->>", "br>", "[ Collect this chapter ]", "[Get Jinjiang Coins for free]", "[Complain]", "Complaint about harmful pornography",
        "Complaints involving minors", "Complaint about data falsification", "Report fake update", "other    Article Collection",
        "Categorize your favorite articles", "+ Added new collection category", "Added Cancel", "Customize favorite categories", "View favorites list", "↑ Back to top",
        "Open Jinjiang App and scan the QR code to read", 
        "Support mobile phone scanning QR code reading  wap reading click: https://m.jjwxc.net/book2/1675875/", "This author currently has no tweets"
    ]
    for filter in filters:
        text = text.replace(filter, "")

    if translate == 1:
        return google_translate(text)
        
    return text if text else None

def get_link_from_id(soup, id_value):
    element = soup.find(id=id_value)
    if element:
        return element.get('href')
    element = soup.find('a', class_=id_value)
    if element:
        return element.get('href')
    return None
    
def get_link_from_class(soup, class_value):
    element = soup.find('a', class_=class_value)
    if element:
        return element.get('href')
    return None

def transformers_translate(text, model_name="Helsinki-NLP/opus-mt-zh-en"):
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    chunks = textwrap.wrap(text, 100)
    translated_text = ""

    for chunk in chunks:
        inputs = tokenizer(chunk, return_tensors="pt")
        translated = model.generate(**inputs)
        tgt_text = [tokenizer.decode(t, skip_special_tokens=True) for t in translated]
        translated_text += tgt_text[0]

    return translated_text if translated_text else None

def google_translate(text):
    translator = Translator(service_urls=['translate.google.com'])
    translated = translator.translate(text, dest='en')
    return translated.text if translated and translated.text else None

# Main execution
url = "https://www.jjwxc.net/onebook.php?novelid=1675875&chapterid=1"
base_url = "https://www.jjwxc.net/onebook.php?novelid=1675875&chapterid="
text_class = "novelbody"
text_id = ""
next_class = "bi"
translate = 0
chapter_index = 1

for i in range(0, 50):
    print(f"Getting Chapter: {chapter_index + i} From {url}")

    soup = get_html_response(url)
    
    text = get_text_from_specific_div(soup, div_class=text_class, div_id=text_id, translate=translate)

    while not text:
        print(f"No text found in {url}, trying again...")
        soup = get_html_response(url)
        text = get_text_from_specific_div(soup, div_class=text_class, div_id=text_id, translate=translate)

    with open(output_file, 'a') as f:
        f.write(f"\n{text}")

    url = base_url + str(chapter_index + i)
    print(f"done\nnext -> {url}")
