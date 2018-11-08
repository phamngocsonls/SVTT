import requests
from bs4 import BeautifulSoup

def start_crawl():
    url = "https://en.oxforddictionaries.com/definition/school"
    #word_list = []
    source = requests.get(url).text
    print("=======================================================================")
    soup = BeautifulSoup(source, 'html.parser')
    #print(source)
    gram_items = soup.find_all('div', {'class' : 'ub'})

    div_items = soup.find_all('div', {'class' : 'p10'})

    for item in div_items:
        #print(item)
        print(item.get_text())
        print("--------------------")

start_crawl()