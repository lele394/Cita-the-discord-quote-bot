import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import os
import random as rd
"""
word = str(input("word"))
page = str(input("page"))
"""
word = 'love'

def citaFinder(word):

    #=============FIRST CALL/FIND MAX PAGE======================
    url = "https://www.goodreads.com/quotes/search?utf8=%E2%9C%93&q" + "1" + '&q=' + word + '&utf8=%E2%9C%93'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    soup2 = soup.find_all("div", {"class":"quoteDetails"})
    #=============PAGE NUMBER MAX=================
    page = soup.find_all("div", {"style":"float: right"})
    page2 = []
    for i in page:
        page2 = i.find_all("a")
    pageNum = int(page2[-2].get_text())
    if pageNum>100:
        pageNum2 = str(rd.randint(1,100))
    else:
        pageNum2 = str(rd.randint(1,pageNum))
    #=====================SECOND CALL/GET CITATIONS===============

    url = 'https://www.goodreads.com/quotes/search?commit=Search&page=' + pageNum2 + '&q=' + word + '&utf8=%E2%9C%93'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    soup2 = soup.find_all("div", {"class":"quoteDetails"})
    res = []
    for i in soup2:
        res.append(i.find_all("div")[0])
    res2 = []
    for i in res:
        res2.append(i.get_text())
    #               ==========DATA MOTHERFUCKER HEHE HERE THEY ARE================
    end = []
    for data in res2:
        if "//<![CDATA[" in data:
            data = data.split("//<![CDATA[")
            end.append(data[0])
        else:
            end.append(data)
    citNum = rd.randint(0,len(end)-1)
    citation = end[citNum] #the whole fcking THINGY


    citData = citation.split("\n")

    cita = citData[1]
    auth = citData[4]

    try:
        source = citData[7]
        return cita,auth,source,pageNum2,citNum
    except IndexError:
        return cita,auth,"Uknown source",pageNum2,citNum


def citaFinderID(word, pageNum, citNum):
    url = 'https://www.goodreads.com/quotes/search?commit=Search&page=' + pageNum + '&q=' + word + '&utf8=%E2%9C%93'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    soup2 = soup.find_all("div", {"class":"quoteDetails"})
    res = []
    for i in soup2:
        res.append(i.find_all("div")[0])
    res2 = []
    for i in res:
        res2.append(i.get_text())
    #               ==========DATA MOTHERFUCKER HEHE HERE THEY ARE================
    end = []
    for data in res2:
        if "//<![CDATA[" in data:
            data = data.split("//<![CDATA[")
            end.append(data[0])
        else:
            end.append(data)

    citation = end[int(citNum)] #the whole fcking THINGY


    citData = citation.split("\n")

    cita = citData[1]
    auth = citData[4]

    try:
        source = citData[7]
        return cita,auth,source,pageNum,citNum
    except IndexError:
        return cita,auth,"Uknown source",pageNum,citNum


#
