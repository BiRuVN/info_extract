# -*- coding: utf-8 -*-
import pandas as pd
import re
from underthesea import pos_tag, sent_tokenize, word_tokenize, ner

def read_txt(f_path):
    f = open(f_path, encoding="utf8")
    if f.mode == 'r':
        content = f.read()
    return content.split('\n')

stopwords = read_txt('stopwords.txt')

# Remove stopwords
def remove_stopword(text):
    tokens = word_tokenize(text)
    return " ".join(word for word in tokens if word not in stopwords)

df = pd.read_csv('chotot.csv')
arr_description = []
set_abbreviate = { 'phòng ngủ': ['pn', 'phn'],
            'phòng khách': ['pk', 'phk'],
            'phòng vệ sinh': ['wc', 'tolet', 'toilet'],
            'hợp đồng': ['hđ', 'hd'],
            'đầy đủ': ['full'],
            'nhỏ': ['mini'],
            'tầm nhìn': ['view'],
            'địa chỉ': ['đc', 'đ/c'],
            'miễn phí': ['free'],
            'vân vân' : ['vv'],
            'liên hệ' : ['lh'],
            'trung tâm thành phố': ['tttp'],
            'yêu cầu': ['order'],
            'công viên': ['cv', 'cvien'],
            'triệu /' : ['tr/', ' tr /', 'tr '],
            'phường' : [' p ', ' ph '],
            'quận' : [' q ', ' qu ']
            }

def replace_abbreviate(s):
    for key in set_abbreviate:
        s = re.sub('|'.join(set_abbreviate[key]),' {} '.format(key), s)
    return s

for index in range(len(df.index)):
    arr = [re.sub('[+|()]', ' ', line.lower()) for line in df.iloc[index]["description"].split('\n')]
    arr = [re.sub('[.]', '', line) for line in arr if line != '']
    arr = [replace_abbreviate(line) for line in arr]
    arr = [re.sub('[^0-9A-Za-z ạảãàáâậầấẩẫăắằặẳẵóòọõỏôộổỗồốơờớợởỡéèẻẹẽêếềệểễúùụủũưựữửừứíìịỉĩýỳỷỵỹđ/%,]', ' ', line) for line in arr]
    arr = [re.sub('m2', ' m2', line) for line in arr]
    arr = [" ".join(line.split()) for line in arr]
    arr_description.append(". ".join(arr))
    
df = df.assign(description_2 = arr_description)

items = read_txt('items.txt')
places = read_txt('places.txt')
num = read_txt('numbers.txt')

places_list = []
items_list = []
numbers_list = []
else_list = []

for text in df['description_2']:
    t = " ".join(remove_stopword(text).split())
    tags = ner(t)
    
    places_temp = []
    items_temp = []
    numbers_temp = []
    else_temp = []
    rm = []
    
    for i in range (len(tags)):
        if tags[i][1] == 'M':
            temp = ''
            for j in range (i, i+5):
                try:
                    temp = temp + ' ' + tags[j][0]
                    if tags[j][1] != 'Nu' and tags[j][1] != 'N':
                        continue
                    else:
                        break
                except IndexError:
                    pass
            if any(character.isdigit() for character in temp):
                numbers_temp.append(temp)
                rm.append(x for x in ner(temp))
        elif any(character.isdigit() for character in tags[i][0]):
            numbers_temp.append(tags[i][0])
        elif tags[i][1] == 'N':
            if any(s in tags[i][0] for s in items):
                items_temp.append(tags[i][0])
            elif any(s in tags[i][0] for s in places):
                places_temp.append(tags[i][0])
            else:
                else_temp.append(tags[i][0])
    
    items_list.append(items_temp)
    places_list.append(places_temp)
    else_list.append(else_temp)
    numbers_list.append(numbers_temp)




