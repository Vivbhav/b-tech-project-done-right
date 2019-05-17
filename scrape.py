#Textract
from googlesearch import search
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup

def scrape(query):
    #query=input("")
    fw = open("GoogleSearchResults", "w")
    output = []
    for j in search(query, tld="co.in", num=5, stop=1, pause=2):
	    #print(j)
            if 'wikipedia' in j:
                #print(j)
                j = j[30:]
                print(j)
                output.append(j)
    #print("End of link gathering phase")
    toreturn = []
    try:
    	response = requests.get('https://en.wikipedia.org/w/api.php',params={'action': 'query','format': 'json', 'titles': output[0], 'prop': 'extracts', 'explaintext': True,}).json()
    	page = next(iter(response['query']['pages'].values()))
    	output = page['extract']
    	lines = output.split('\n')
    	fw = open("WikiResults", "w")
    	for line in lines:
    	    if '==' in line or line == '' or len(line) < 75:
    	        pass
    	    else:
                toreturn.append(line)
    	        #fw.write(line + '\n')
    except KeyError:
	    print("Information for such a topic doesn't exist.")
    #print(toreturn[0])
    return toreturn

if __name__ == "__main__":
    scrape(input(""))
