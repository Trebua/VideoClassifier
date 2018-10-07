# coding=utf-8

import urllib
import wget
import json

#Funksjonen lagrer video av LAV kvalitet (kan endres til høy) fra TED-talks
#dwn_link:"https://www.ted.com/talks/ken_robinson_says_schools_kill_creativity"
#to_path: /videos/vid1..vid2 etc
def download_video(dwn_link, to_path):
    #Henter hele HTML-til dwn_link
    rsp = urllib.urlopen(dwn_link)
    rsp_text = rsp.read()

    #Finner url for direkte nedlastning med litt triksing
    start_index = rsp_text.index('"nativeDownloads":{"low":'.encode())
    stop_index = rsp_text.index('"medium":"http'.encode())-1
    url = rsp_text[start_index:stop_index:].decode()
    url = url.replace('"nativeDownloads":{"low":', "")
    url = url[1:-1]

    #Laster ned urlen fra forrige steg til to_path
    wget.download(url, to_path)

#Laster ned engelske subtitles vha id i datasett. Kan endres til andre språk
def download_subtitles(id, lang = "en"):
    try:
        url = f"https://www.ted.com/talks/subtitles/id/{id}/lang/{lang}"
        hdr = {'User-agent': 'your bot 0.1'} #stygg workaround for rate-limiting
        req = urllib.request.Request(url, headers=hdr)
        rsp = urllib.request.urlopen(req)
        rsp_text = rsp.read().decode()
        d = json.loads(rsp_text)
        text = text_from_dict(d)
        return text
    except Exception as e: 
        print(e)
        return ""

#Renser tekst, kan forbedres
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
            txt += content + " "
    return txt