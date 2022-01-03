#!/bin/python3

from time import time
#from os import chdir
import urllib
from bs4 import BeautifulSoup
import json

#chdir("/home/robin/Documents/Python/arxivnotif/")

from utilities import *
from notify import desktopNotification


subscriptions = open("subscriptions.txt", "r")          #the subscription file should contain the names of the authors as 'lastname, firstname'

fp = open("publications.html", "w")            #write publications info in an html document
html_body = ""

newPublications = False

for friend in sorted(subscriptions.readlines()):

# Fetch the html files
    response = urllib.request.urlopen("https://arxiv.org/search/?searchtype=all&query="+urllib.parse.quote_plus('{}'.format(friend[:-1]))+"&abstracts=show&size=50&order=-submitted_date")
    html_page = response.read()


    soup = BeautifulSoup(html_page, "html.parser")      # Parse the html file with BeautifulSoup

    dates=[]
    
    for x in soup.ol.find_all('li'):
        dates.append(cleanDate(x.find(string='Submitted').next_element.string))         #Extract the publication dates from the arxiv search
    
    
    filepath = "data/{}/".format(friend[:-1])
    
    try:
        file1 = open(filepath+"lastcheck", "r")            #Try to open the file with old publication dates
    except FileNotFoundError:                              #If needed, create the data folders and timestamp file
        if not os.path.exists(filepath):
            createDataFolder(friend[:-1])
        with open(filepath+"lastcheck", "w") as file1:        
            json.dump(dateToFloat(dates[0]), file1)         #When a new author is added to the subscriptions, show their latest publication


    with open("data/{}/lastcheck".format(friend[:-1]), "r") as file1:
        lastcheck = json.load(file1)
        
    isNew = []
    for d in dates:
        if dateToFloat(d) >= lastcheck:
            isNew.append(True)
        else: 
            isNew.append(False) 

    if any(isNew):            #checks if there have been new publications since last time the program was run
        newPublications = True
        title=[]
        abstract=[]
        link=[]
        authors=[]

        for x in soup.ol.find_all('li'):                #extract new publications info from the arxiv search
            title.append(x.find('p', class_='title is-5 mathjax').string)
            abstract.append(x.find('span', class_='abstract-full has-text-grey-dark mathjax').next_element.string)
            link.append('https://arxiv.org/abs/'+x.find('a').string[6:])
            pub_authors = []
            for y in x.find('p', class_ = 'authors').find_all('a'):
                pub_authors.append(y.string)
            authors.append(pub_authors)

        #print("New publications!")
        new_dates = [item for item, b in zip(dates, isNew) if b]
        new_titles = [item for item, b in zip(title, isNew) if b]
        new_abstracts = [item for item, b in zip(abstract, isNew) if b]
        new_links = [item for item, b in zip(link, isNew) if b]
        new_authors = [item for item, b in zip(authors, isNew) if b]


        html_body += "<h2>Lastest articles by {} on arXiv </h2><ul>".format(formatName(friend))

        for d, t, abst, auth, link in zip(new_dates, new_titles, new_abstracts, new_authors, new_links):
            t = t.strip()
            auth_list = ''
            i = 0
            while i < len(auth)-1:
                auth_list += auth[i]+', '
                i+=1
            auth_list += auth[i]

            html_body += '''<li>
        <p>
        <b><a style="font-size:120%;text-decoration:none;color:#086db1;" href={}> {} </a></b>
        </p>
        <p>
        <span style="color:#287916;background-color:#eeffe8"><b> Authors:</b> </span>
        {}
        </p> 
        <p>
        <span> 
        <b>Abstract:</b> {} 
        </span>
        </p>
        <p style = "font-size:85%;"><b>Submitted:</b> </span> {}
        <br><br><br></p></li>'''.format(link,t, auth_list, abst, d)
        
        #with open(filepath+"lastcheck", "w") as file2:
            #json.dump(time(), file2)
   
    if any(isNew):
        html_body += "</ul><hr>"
    
if newPublications:
    html = htmlCoat(html_body)
    fp.write(html)
    desktopNotification()
    
fp.close()
