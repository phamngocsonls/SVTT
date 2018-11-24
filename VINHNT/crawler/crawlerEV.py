import os
import sys
import requests
from bs4 import BeautifulSoup
import re
import pymongo
from pymongo import MongoClient
import pprint

#client = MongoClient()      # Defaul connection port 27017
client = MongoClient('mongodb://localhost:27017/')
#client = MongoClient('localhost', 27017)

############### Getting database
db = client.Dictionary_database
#db = client['test_database']

############### Getting  a colection
collettion = db.Dictionary_database
#collection = db['test_collection']

def extract_data(tag_name, fh):
    list_ex = []
    list_exam = []
    defs = "none"
    for e in tag_name.children:
        if (str(e.name) == 'p'):
            d = e.find('span', {'class' : 'ind'})           # extract definition
            defs = d.get_text()
            print(d.get_text(), file=fh)
        try:
            if str(e['class']) == str(['exg']):     # extract example
                print("ex:", file=fh)
                print(e.get_text(), file=fh)
                exam = e.get_text()
                list_exam.append(exam)
        except: 
            continue
        if str(e['class']) == str(['examples']):        # extract more example
            exs = e.find_all('li', {'class':'ex'})
            print("MORE EXAMPLES", file=fh)
            for ex in exs:
                list_ex.append(ex.get_text())
                print(ex.get_text(), file=fh)
                #print(ex.get_text())
    #print(list_ex)
    example = {
        "exam": list_exam,
        "more_ex": list_ex
    }
    return defs, example

def has_href_no_name(tag):
    return tag.has_attr('href') and not tag.has_attr('name')

def has_no_style(tag):
    return not tag.has_attr('style')


os.system("mkdir EV")
os.system("mkdir EV/oxford")
fd = open('oxford_data1', 'r')
os.system("mkdir EV/soha")
os.system("mkdir EV/coviet")

data = fd.readlines()
num_words = 0
'''oxford = {}
soha = {}
coviet = {}'''
posts = db.posts

for line in data:
    word = re.search('(.+?)\n', line).group(1)
    print(f"----{word}---------")
    num_words +=1
    if num_words == 5:
        break
    
    ####################### Crawl from oxford
    try:
        print("Num of word crawl from oxford: ", num_words)
        url = 'https://en.oxforddictionaries.com/definition/' + word
        fh = open('EV/oxford/'+str(num_words)+' '+word+'.txt', 'w')
        print(str(word).center(50, ' '), file=fh)
        print('='.center(50, '='), file=fh)
        source = requests.get(url).text
        soup = BeautifulSoup(source, 'lxml')
        div_entry = soup.find('div', {'class' : 'entryWrapper'})                    #find div tag
        sec_grams = div_entry.find_all('section', {'class' : 'gramb'})      # find section tag set
        list_gram = []
        for gram in sec_grams:
            for child in gram.children:
                if (str(child.name) == 'h3'):
                    type_gram = child.get_text()
                    print(f"[{child.get_text()}]", end=' ', file=fh)
                if (str(child.name) == 'ul'):
                    trg = child.find('div', {'class' : 'trg'})
                    w_def, example = extract_data(trg, fh)
                    list_sub = []
                    for t in trg.children:
                        subSenses = t.find_all('li', {'class' : 'subSense'})
                        for sub in subSenses:
                            for s in sub.children:
                                if str(s.name) == 'span':
                                    subdef = s.get_text()
                                    print(s.get_text(), file=fh)
                                try:
                                    if str(s['class']) == str(['trg']):
                                        su, subex = extract_data(s, fh)
                                except:
                                        continue
                            sub_m = {"sub_def": subdef, "sub_exam": subex}
                            list_sub.append(sub_m)
            gram = {"type": type_gram, "def": w_def, "exam": example, "subSense": list_sub}
            list_gram.append(gram)
        pronun = soup.find_all('span', {'class':'phoneticspelling'})
        pron = pronun[0].get_text()
        oxford = {
            "word": word, 
            "pron": pron,
            "gram": list_gram
        }
        #post_id = posts.insert_one(post).inserted_id
        #print(post_id)
        fh.close()
    except:
        oxford = {}

    ####################### Crawl from tratu.soha.vn
    try:
        url = "http://tratu.soha.vn/dict/en_vn/" + word
        #print(url)
        fw = open('EV/soha/'+str(num_words)+' '+word+'.txt', 'w')
        print(word.center(50, ' '), file=fw)
        print('='.center(50, '='), file=fw)
        source = requests.get(url).text
        soup = BeautifulSoup(source, 'lxml')
        contents = soup.find_all('div', {'id':'bodyContent'})
        sub_bodyContent = contents[0].find('div', {'id': 'content-5'})
        pron = sub_bodyContent.find_all('b')
        print(pron[0].get_text(), file=fw)
        content2s = contents[0].find_all('div', {'class': 'section-h2'})
        ct2_set = []
        for content2 in content2s:
            #print(content2)
            h2 = content2.find('h2').get_text()
            content3s = content2.find_all('div', {'class':'section-h3'})
            ct3_set = []
            for content3 in content3s:
                h3 = content3.find('h3').get_text()
                print(h3, file=fw)
                content5s = content3.find_all('div', {'class': 'section-h5'})
                ct5_set = []
                examsoha = []
                for content5 in content5s:
                    h5 = content5.find('h5').get_text()
                    print(h5, file=fw)
                    dd = content5.find_all('dd')
                    try:
                        if dd[0].find('dl') is None:
                            print(dd[0].get_text(), file=fw)        # dong nghia
                            examsoha = dd[0].get_text()
                        else:
                            print((dd[0].find('dl')).get_text(), file=fw)       # exam
                            sub_dd = dd[0].find_all('dd')
                            for each in sub_dd:
                                ex = each.get_text()
                                examsoha.append(ex)
                    except:
                        pass
                    ct5 = {"h5": h5, "exam": examsoha}
                    ct5_set.append(ct5)
                ct3 = { "h3": h3, "ct5_set": ct5_set}
                ct3_set.append(ct3)
            ct2 = {"h2": h2, "ct3_set": ct3_set}
            ct2_set.append(ct2)
            #print(ct2_set)
        soha = {
            "word": word,
            "pron": pron[0].get_text(),
            "ct2_set": ct2_set
        }
        #post_id = posts.insert_one(soha).inserted_id
        #print(post_id)
        fw.close()
    except:
        soha = {}
    
    ####################### Crawl from tratu.coviet.vn
    try:
        url = 'http://tratu.coviet.vn/hoc-tieng-anh/tu-dien/lac-viet/A-V/'+word+'.html'
        fc = open('EV/coviet/'+str(num_words)+' '+word+'.txt', 'w')
        print(word.center(50, ' '), file=fc)
        print('='.center(50, '='), file=fc)
        source = requests.get(url).text
        soup = BeautifulSoup(source, 'lxml')
        pron_tag = soup.find_all('div', {'class': 'p5l fl cB'})
        pron = pron_tag[0].get_text()
        print(pron, file = fc)
        content_tag = soup.find_all('div', {'class': 'p10'})
        examc_set = []
        
        partofspeech_set = []
        gram = "none"
        for partofspeech in content_tag[1].children:
            #print(len(partofspeech))
            sub_ct_set = []
            for each in partofspeech.children:
                if each.name == "div":
                    attr = str(each['class'])
                    if attr == str(['ub']):
                        #print(each.get_text(), file=fc)
                        gram = each.get_text()
                    if attr == str(['m']):
                        def_m = each.get_text()
                        print(def_m, file=fc)
                        examc_set = []
                        ex_set = each.find_next_siblings()
                        for ex in ex_set:
                            if str(ex['class']) == str(['m']):
                                break
                            else:
                                print(ex.get_text(), file=fc)
                                examc_set.append(ex.get_text())
                        sub_ct = {"sub_def": def_m, "exam": examc_set}
                        sub_ct_set.append(sub_ct)
                elif each.name == 'a':
                    print(each.get_text(), file=fc)
                    sub_ct_set.append(each.get_text())
            pos = {"gram": gram, "subct": sub_ct_set}
            #print(pos)
            partofspeech_set.append(pos)
        #print(partofspeech_set)
        coviet = {
            "word": word,
            "pron": pron, 
            "partofspeech": partofspeech_set
        }
        fc.close()
        #posts.insert_one(coviet).inserted_id
    except:
        coviet = {}
    ob = {
        "word_name": word,
        "oxford": oxford,
        "soha": soha,
        "coviet": coviet
    }
    posts.insert_one(ob).inserted_id

pprint.pprint(posts.find_one({"word_name": "a"}))
posts.delete_many({})
