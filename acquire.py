from requests import get
from bs4 import BeautifulSoup
import os
import re
import json

def get_article(url):
    headers = {'User-Agent': 'Codeup Data Science'}
    response = get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.select('.entry-title')[0].text
    content = soup.select('.entry-content')[0].text
    output = {
        'title':title.strip(),
        'content':content.strip()
    }
    return output

def get_blog_articles(url_list):
    output = []
    for url in url_list:
        article_dict = get_article(url)
        output.append(article_dict)
    return output

def get_articles(url, category):
    headers = {'User-Agent': 'Codeup Data Science'}
    outputs = []
    response = get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    news_cards = soup.select('.news-card')
    for card in news_cards:
        title = card.select('.news-card-title')[0].text
        title = re.findall('(\s.*)', title)[1]
        content = card.select('.news-card-content')[0].text
        output = {
            'title':title.strip(),
            'content':content.strip(),
            'category':category
        }
        outputs.append(output)
    return outputs

def get_news_articles():
    outputs = []
    base_url = 'https://inshorts.com/en/read'
    end_points = ['business', 'sports', 'technology', 'entertainment'] 
    for endp in end_points:
        outputs += get_articles(f"{base_url}/{endp}", endp)
    return outputs

def cache_data(dictionary, filename='cache_file.json'):
    json_obj = json.dumps(dictionary, indent = 4)
    try:
        with open(filename, 'w') as f:
            f.write(json_obj)
        return True
    except Exception as e:
        print(e)
        return False
    
def read_url_or_file_inshort(filename='inshort_articles.json', query_url=False):
    if os.path.isfile(filename) and not query_url:
        print('Found File')
        try:
            with open(filename, 'r') as f:
                json_obj = json.load(f)
            return json_obj
        except Exception as e:
            print(e)
            return None
    else:
        print('Querying url')
        try:
            dictionary = get_news_articles()
            cache_data(dictionary, filename=filename)
            return dictionary
        except Exception as e:
            print(e)
            return None
            
def read_url_or_file_codeup(filename='codeup_articles.json', query_url=False):
    if os.path.isfile(filename) and not query_url:
        print('Found File')
        try:
            with open(filename, 'r') as f:
                json_obj = json.load(f)
            return json_obj
        except Exception as e:
            print(e)
            return None
    else:
        print('Querying url')
        url_1 = 'https://codeup.com/tips-for-prospective-students/is-our-cloud-administration-program-right-for-you/'
        url_2 = 'https://codeup.com/workshops/pride-in-tech-panel/'
        url_3 = 'https://codeup.com/tips-for-prospective-students/mental-health-first-aid-training/'
        url_4 = 'https://codeup.com/workshops/codeup-dallas-how-to-succeed-at-a-coding-bootcamp-on-june-9th/'
        url_5 = 'https://codeup.com/featured/our-acquisition-of-the-rackspace-cloud-academy-one-year-later/'
        select_articles = [url_1, url_2, url_3, url_4, url_5]
        try:
            dictionary = get_blog_articles(select_articles)
            cache_data(dictionary, filename=filename)
            return dictionary
        except Exception as e:
            print(e)
            return None