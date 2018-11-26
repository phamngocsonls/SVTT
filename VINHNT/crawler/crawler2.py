import os
import sys
import requests
from bs4 import BeautifulSoup

import os
import sys
import requests
from bs4 import BeautifulSoup


print('='.center(40, '='))
print("Start crawling data from tratu.soha.vn")
print('='.center(40, '='))

os.system("mkdir A-V")
os.system("mkdir A-V/oxford")
os.system("mkdir A-V/tratu")

NUM_OF_WORD = 1

word = "go"
queue_words = []
list_word = []
flag = 1
num_words = len(list_word)

def has_href_no_name(tag):
    return tag.has_attr('href') and not tag.has_attr('name')

def has_no_style(tag):
    return not tag.has_attr('style')

while num_words < 10 and flag == 1:
    list_word.append(word)
    num_words = len(list_word)
    
    url = "http://tratu.soha.vn/dict/en_vn/" + word
    fw = open('A-V/tratu/'+str(num_words)+'_'+word+'.txt', 'w')
    print('='.center(50, '='), file=fw)
    print(word.center(50, ' '), file=fw)
    print('='.center(50, '='), file=fw)
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    contents = soup.find_all('div', {'class':'section-h2'})

    for ctn in contents:
        for first_child in ctn.children:
            if first_child.name == 'h2':
                print('-'.center(50, '-'), file=fw)
                print(first_child.get_text(), file=fw)
                print('-'.center(50, '-'), file=fw)
            if first_child.name == 'div':               #content 3
                for sec_child in first_child.children:  #content 5
                    if sec_child.name == 'h3':
                        print(f"[ {sec_child.get_text()} ]", file=fw)
                    if sec_child.name == 'div':
                        h5 = sec_child.find_all('h5')
                        print(h5[0].get_text(), file=fw)
                        '''try:
                            dl = sec_child.find_all('dl')
                            print(f"--{dl[1].get_text()}", file=fw)
                        except:
                            continue'''
                        dd = sec_child.find_all('dd')
                        try:
                            if dd[0].find('dl') is None:
                                print(dd[0].get_text(), file=fw)
                            else:
                                print((dd[0].find('dl')).get_text(), file=fw)
                        except:
                            continue
                        urls = sec_child.find_all(has_href_no_name)
                        for url in urls:
                            u = url.get_text()
                            if u in list_word:
                                continue
                            elif u in queue_words:
                                continue
                            elif len(queue_words) > 100:
                                continue
                            else:
                                queue_words.append(u)
    word = queue_words[0]
    del queue_words[0]
    if len(queue_words) == 0:
        flag = 0
        print("Hang doi rong !!!")
    else:
        print("NUM OF WORD: ", num_words)
        print("LENGTH OF QUEUE: ", len(queue_words))
    fw.close()



print("=".center(40, '='))
print("DONE".center(40, ' '))
print('='.center(40, '='))
print("Start crawling data from https://en.oxforddictionaries.com")
print('='.center(40, '='))

def extract_data(tag_name, fw):
        for e in tag_name.children:
                if (str(e.name) == 'p'):
                        d = e.find('span', {'class' : 'ind'})           # extract definition
                        print(d.get_text(), file=fh)
                try:
                        if str(e['class']) == str(['exg']):     # extract example
                                print("ex:", file=fh)
                                print(e.get_text(), file=fh)
                except: 
                        continue
                if str(e['class']) == str(['examples']):        # extract more example
                        exs = e.find_all('li', {'class':'ex'})
                        print("MORE EXAMPLES", file=fh)
                        for ex in exs:
                                print(ex.get_text(), file=fh)


num_words_oxford = 0

for each_word in list_word:
    try:
        num_words_oxford +=1
        print("Num of word crawl from oxford: ", num_words_oxford)
        url = 'https://en.oxforddictionaries.com/definition/' + each_word
        fh = open('A-V/oxford/'+str(num_words_oxford)+' '+each_word+'.txt', 'w')
        print('='.center(50, '='), file=fh)
        print(str(each_word).center(50, ' '), file=fh)
        print('='.center(50, '='), file=fh)
        source = requests.get(url).text
        soup = BeautifulSoup(source, 'lxml')
        div_entry = soup.find('div', {'class' : 'entryWrapper'})                    #find div tag
        #print(type(div_entry))
        #print(div_entry.get_text())
        sec_grams = div_entry.find_all('section', {'class' : 'gramb'})      # find section tag set
        num_type = 0
        for gram in sec_grams:
            for child in gram.children:
                #print(type(child))
                #print(child.name)
                if (str(child.name) == 'h3'):
                    print(f"[{child.get_text()}]", end=' ', file=fh)
                if (str(child.name) == 'ul'):
                    trg = child.find('div', {'class' : 'trg'})
                    extract_data(trg, fh)
                    
                    for t in trg.children:
                        subSenses = t.find_all('li', {'class' : 'subSense'})
                        #extract_data(subSenses)
                        for sub in subSenses:
                            for s in sub.children:
                                if str(s.name) == 'span':
                                    print(s.get_text(), file=fh)
                                try:
                                    if str(s['class']) == str(['trg']):
                                        extract_data(s, fh)
                                except:
                                        continue
        fh.close()
    except:
            continue