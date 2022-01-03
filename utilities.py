import os
from time import mktime, strptime, strftime
import locale

def formatName(raw_name):
    index = raw_name.find(',')
    name = raw_name[index+1:]+' '+raw_name[:index]
    return name

def cleanDate(date):
	for i, j in {" ":"", ";":"", "\n":""}.items():
		date = date.replace(i, j)
	locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
	date = strftime("%d %B %Y" , strptime(date, "%d%B,%Y"))
	return date

def dateToFloat(date):
	return mktime(strptime(date, "%d %B %Y"))

def htmlCoat(html_body):
    html = """<html>
        <head>
        <script>
        MathJax = {
        tex: {
            inlineMath: [['$', '$']]
            }
        };
        </script>
        <script type="text/javascript" id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
        <title> arXiv notifications </title>
        </head>
        <body style = "font-size:14px;font-family: Helvetica;">
        """+ html_body + "</main></body></html>"
    return html

def createDataFolder(name):
    os.makedirs("data/{}/".format(name))

