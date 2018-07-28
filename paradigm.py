import os
import re
import itertools
from itertools import chain
import lxml
import lxml.html
import unicodedata

homeDir = os.getenv("HOME")
rootDir = os.path.join(homeDir,"core_paradigm")
usukDir = os.path.join(rootDir,"us2uk")
us_dir = os.path.join(usukDir,"US_words.txt")
uk_dir = os.path.join(usukDir,"UK_words.txt")


def clean_txt(txt_path,regex=None):
    if regex is None:
        regex = re.compile(r'([^a-z\- ])|((^| ). )')

    output = [line.strip() for line in open(txt_path,"r")] 
    output = [[word.lower() for word in text.split()] for text in output]
    output = list(itertools.chain.from_iterable(output))
    output = ' '.join(str(x) for x in output)
    output = lxml.html.fromstring(output).text_content() #removing weird html stuff
    output = regex.sub('',output)
    output = regex.sub('',output)
    standardiz_s(output,us_dir,uk_dir) 


def preprocessFiles(rootDir):
    text = []
    for dirname, subdirname, files in os.walk(rootDir):
        for f in files:
            if f.endswith('.txt'):
                try:
                    path = os.path.join(dirname,f)
                    text.append(clean_txt(path))
                except:
                    print(path)
    return text


#standardizes UK and US spelling
def standardiz_s(string_input,us_dir,uk_dir):
    #getting US/UK word lists

    with open(uk_dir, 'r') as f:    
        UK = f.read().replace('\u2028',' ').replace('\xa0','').splitlines()
        UK = UK[0].split()
    
    with open(us_dir, 'r') as f:    
        US = f.read().replace('\u2028',' ').replace('\xa0','').splitlines()
        US  = US[0].split()
    
    for us_ind in range(len(US)):
        if US[us_ind] in string_input:
            string_input = string_input.replace(US[us_ind], UK[us_ind])
    return(string_input)

#cleanup for NBER texts
def cleanNBER(textList):
    pattern=re.compile(".*?abstract(.*?)(?:references|bibliography|$).*") 
    problem = [] #697/17647 nber papers were problems

    for i in range(len(textList)):
        try:
            textList[i] = re.match(pattern,textList[i]).group(1)
        except:
            problem.append(i)
    return(textList)
