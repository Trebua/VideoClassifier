# coding=utf-8

from urllib.request import urlopen
import json


#Denne metoden kan kansjke endres til å bruke request-bibl istedet?
def download_subtitles(id, to_path, lang = "en", additional_text = ""):
    url = f"https://www.ted.com/talks/subtitles/id/{id}/lang/{lang}"
    #Henter hele HTML-til dwn_link
    rsp = urlopen(url)
    rsp_text = rsp.read().decode()
    d = json.loads(rsp_text)
    text = text_from_dict(d)
    f = open(to_path, "w")
    f.write(additional_text + "---" + text)
    f.close()

def text_from_dict(dict):
    l = dict["captions"]
    illegal = ["(Laughter)","(Applause)"]
    txt = ""
    for d in l:
        if d["content"] in illegal:
            continue
        if d["content"] not in illegal:
            content = d["content"]
            content = "".join([i for i in content if i.isalpha() or i == " " or i == "\n"])
            #her kan "\n" replaces med " "
            txt += content + " "
    return txt
    
#download_subtitles(1, "subtitles/test.txt")