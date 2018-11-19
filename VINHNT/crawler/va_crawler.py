import requests
from bs4 import BeautifulSoup
import sys
import os
list_words = []

print('='.center(40, '='))
print("Start crawling data from http://tratu.coviet.vn")
print('='.center(40, '='))

os.system("mkdir tratu.coviet")
fname  = open('tratu.coviet/word_name.txt', 'w')
fdef   = open('tratu.coviet/word_def.txt', 'w')

word = "home"
queue_words = []
flag = 1

while (len(list_words) < 5000) and (flag > 0):
        url = "http://tratu.coviet.vn/hoc-tieng-anh/tu-dien/lac-viet/A-V/"+str(word)+".html"
        list_words.append(word)
        source = requests.get(url).text
        soup = BeautifulSoup(source, 'lxml')
        partofspeech = [0, 1, 2, 3, 4, 100]
        num_words = str(len(list_words))
        print(f"{num_words} {word}", file=fname)
        for index in partofspeech:
                div_par = soup.find_all('div', {'id' : 'partofspeech_'+str(index)})
                
                for item in div_par:
                        #print(item.contents)
                        list_urls = item.find_all('a')          # extract link
                        for e in list_urls:
                                w = e.get_text()
                                w.lower()
                                if w in list_words:
                                        continue
                                elif w in queue_words:
                                        continue
                                elif len(queue_words) > 100:
                                        continue
                                else:
                                        queue_words.append(w)
                        ub = item.find('div', {'class' : 'ub'})         #find type of word: adj adv n ...
                        try:
                                print(f'{num_words} {ub.get_text()}', file=fdef)
                        except:
                                print(f'{num_words} - Don''t exists data', file=fdef)
                        m = item.find_all('div', {'class' : 'm'})       #find define of word
                        for each_m in m:
                                print(f"*{each_m.get_text()}", file=fdef)
                                try:
                                        e = each_m.next_sibling
                                        print(f"--- {e.get_text()}", file=fdef)
                                except:
                                        print(f"--- Do not exists data", file=fdef)
                                try:
                                        em = e.next_sibling
                                        print(f"--- {em.get_text()}", file=fdef)
                                except: 
                                        print(f"--- Do not exists data", file=fdef)
        #list_words.sort()
        #print(list_words)
        print('-'.center(40, '-'))
        print("Num of word in queue:     ", len(queue_words))
        print("Num of word in list_word: ", len(list_words))
        print('-'.center(40, '-'))
        #print(queue_words)
        word = queue_words[0]
        del queue_words[0]
        if len(queue_words) == 0:
                flag = 0
                print("Hang doi rong !!!")
fdef.close()
fname.close()

print("=".center(40, '='))
print("DONE".center(40, ' '))
print('='.center(40, '='))
print("Start crawling data from https://en.oxforddictionaries.com")
print('='.center(40, '='))

os.system("mkdir oxford")
#fname_o  = open('oxford/word_name.txt', 'w')
#fdef_o   = open('oxford/word_def.txt', 'w')
def extract_data(tag_name, fw):
        for e in tag_name.children:
                if (str(e.name) == 'p'):
                        d = e.find('span', {'class' : 'ind'})           # extract definition
                        print(d.get_text(), file=fw)
                try:
                        if str(e['class']) == str(['exg']):     # extract example
                                print("ex:", file=fw)
                                print(e.get_text(), file=fw)
                except: 
                        continue
                if str(e['class']) == str(['examples']):        # extract more example
                        exs = e.find_all('li', {'class':'ex'})
                        print("MORE EXAMPLES", file=fw)
                        for ex in exs:
                                print(ex.get_text(), file=fw)



for each_word in list_words:
        print('len of list word: ', len(list_words))
        try:
                url = 'https://en.oxforddictionaries.com/definition/' + each_word
                fw = open('oxford/'+str(each_word)+'.txt', 'w')
                print('='.center(40, '='), file=fw)
                print(str(each_word).center(40, ' '), file=fw)
                print('='.center(40, '='), file=fw)
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
                                        print(f"[{child.get_text()}]", end=' ', file=fw)
                                if (str(child.name) == 'ul'):
                                        trg = child.find('div', {'class' : 'trg'})
                                        extract_data(trg, fw)
                                        
                                        for t in trg.children:
                                                subSenses = t.find_all('li', {'class' : 'subSense'})
                                                #extract_data(subSenses)
                                                for sub in subSenses:
                                                        for s in sub.children:
                                                                if str(s.name) == 'span':
                                                                        print(s.get_text(), file=fw)
                                                                try:
                                                                        if str(s['class']) == str(['trg']):
                                                                                extract_data(s, fw)
                                                                except:
                                                                        continue
                fw.close()
        except:
                continue