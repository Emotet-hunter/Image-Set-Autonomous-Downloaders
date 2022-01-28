# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 12:15:37 2022

@author: Miguel Peidro Paredes
"""

#Scrapping
from bs4 import BeautifulSoup
import os
import shutil

#Bypass CloudFlare
import cloudscraper

#Change working directory to the External Drive
path = "Download Path"
os.chdir(path)

#CloudFlare Bypass
scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance


#Scrapping Path
header = 'https://www.xtrafondos.com/buscar/'

#Theme Request
print("What images do you want to download?:")
theme = input()

while(True):

    #Proportions Request
    print("Do you want to filter by proportion?")
    print("n -> none")
    print("h -> horizontal")
    print("v -> vertical")
    
    ori = input()
    
    if (ori == "n"):
        break
    elif (ori == "h"):
        break
    elif (ori == "v"):
        break
    
    else:
        ("Wrong input")
    
    

#Requesting result pages number
url = header + theme

pag_num =""

for i in range (1, 10):
    try:    
        result_pages = scraper.get(url, timeout=10)
    except:
        continue
        
    try:
        #Soup Results
        soup = BeautifulSoup(result_pages.text, 'html.parser')
        
        title = str(soup.findAll('h1', attrs={'class' : 'titlepages'})[0].get_text())
        
        #Not Results
        if "no ha coincidido con ningún fondo" in title:
            break
        else:
            pag_num = "0"
        
        for pages in soup.findAll('div', attrs={'class' : 'content-links-pagination'}):
            pag_num = pages.find_all("a")[-1].get_text()
            
        #Results found
        if (pag_num.isnumeric()):
            break
            
    except:
        continue
    
print(pag_num)

 
if (pag_num.isnumeric()):
    
    if (pag_num == "0"):
        print("Just One Page")
        
    else:
        
        count = 0
        
        for i in range (1, int(pag_num)+1):
            
            if (ori == "n"):
                url = header + theme + '/' + str(i)
                
            elif (ori == "h"):
                url = header + theme + "/horizontal/" + str(i)
                
            elif (ori == "v"):
                url = header + theme + "/vertical/" + str(i)
            
            
            try:    
                results = scraper.get(url, timeout=10)
            except:
                print("Unreached Results")
                
            #Soup Results
            soup = BeautifulSoup(results.text, 'html.parser')
            
            #Select Main content
            for maincontent in soup.findAll('div', attrs={'id' : 'pluswall'}):
                
                for url_ext in maincontent.findAll('a', href=True):
                    
                    print (url_ext['href'])
                    
                    try:    
                        results = scraper.get(url_ext['href'], timeout=10)
                    except:
                        print("Unreached Results")
                    
                    #Soup Results
                    img_soup = BeautifulSoup(results.text, 'html.parser')
                    
                    for button in img_soup.findAll('div', attrs={'class' : 'downl'}):
                        
                        download_url = button.findAll('a', href=True)[0]['href']
                        
                        try:
                            
                            file_name = "wallpaper" + str(count) +'.jpg'
                        
                            with open(file_name, 'wb') as f:
                                img = scraper.get(download_url, stream=True)
                                img.raw.decode_content = True
                                shutil.copyfileobj(img.raw, f)
                                
                        
                        except Exception as e:
                            print(e)
                        
                        
                        
                        count += 1
                    
else:
    print("No results")