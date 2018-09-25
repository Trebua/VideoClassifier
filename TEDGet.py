# coding=utf-8

from urllib.request import urlopen
import wget #må lastes ned med pip
#Funksjonen lagrer video av LAV kvalitet (kan endres til høy eller medium) fra TED-talks
#dwn_link:"https://www.ted.com/talks/ken_robinson_says_schools_kill_creativity"
#to_path: /videos/vid1..vid2 etc
def download_ted(dwn_link, to_path):
    #Henter hele HTML-til dwn_link
    rsp = urlopen(dwn_link)
    rsp_text = rsp.read()

    #Finner url for direkte nedlastning med litt triksing
    start_index = rsp_text.index('"nativeDownloads":{"low":'.encode())
    stop_index = rsp_text.index('"medium":"http'.encode())-1
    url = rsp_text[start_index:stop_index:].decode()
    url = url.replace('"nativeDownloads":{"low":', "")
    url = url[1:-1]

    #Laster ned urlen fra forrige steg til to_path
    wget.download(url, to_path)