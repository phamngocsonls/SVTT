import re
d = 0
fr = open('oxford_data', 'r')
fh = open('oxford_data1', 'w')
data = fr.readlines()
word_list = []

for line in data:
    #print(str(line))
    #print(type(line))
    #print(line)
    try:
        a = re.search('(.+?) \n', line).group(1)
        if a in word_list:
            continue
        else:
            try:
                a= a.replace(' ', '-')
            except:
                pass
            print(a, file=fh)
            word_list.append(a)
            d +=1
            continue 
    except:
        pass
    try:
        a = re.search(' (.+?)\n', line).group(1)
        if a in word_list:
            continue
        else:
            try:
                a= a.replace(' ', '-')
            except:
                pass
            print(a, file=fh)
            word_list.append(a)
            d +=1
    except:
        pass

print("DDDDDDDDDDDDd = ", d)
