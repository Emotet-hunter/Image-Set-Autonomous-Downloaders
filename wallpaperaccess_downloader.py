# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 14:39:24 2022

@author: Miguel Peidro Paredes
"""

#Scrapping
from bs4 import BeautifulSoup
import os
import shutil
from PIL import Image

#Bypass CloudFlare
import cloudscraper

#Change working directory to the External Drive
path = "Download Path"
os.chdir(path)

#CloudFlare Bypass
scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance


#Scrapping Path
header = 'https://wallpaperaccess.com/'

#Theme Request
print("What images do you want to download?:")
theme = input()

while(True):

    #Proportions Request
    print("Do you want to filter by proportion? (S/N):")
    
    filt = input()
          
    if (filt == "S" or filt == "s"):
          
        print("ntroduce proportion as minimum (width/height) - maximum (width/height)")
        print()
        print("Example: If you want to download desktop image, the proportion you want is 1,77777778, you can specify (Input: 1.7-1.8)")
        
        proportion = input()
        
        #Extract proportions
        try:
        
            proportion = proportion.split('-')
            
            min_prop = float(proportion[0])
            max_prop = float(proportion[1])
            
            if (isinstance(min_prop, float) and isinstance(max_prop, float)):
                break
            else:
                print("Wrong input")
            
        except:
            proportion_error = True
            
    elif (filt == "N" or filt == "n"):
        break
    

url = header + theme

#Arry of urls requested
urls_array = []

try:    
    results = scraper.get(url, timeout=10)
except:
    print("Unreached Results")
        

#Soup Results
soup = BeautifulSoup(results.text, 'html.parser')

#Select Main content
for maincontent in soup.findAll('div', attrs={'id' : 'maincontent'}):
    
    count = 0
    previous = ""
    
    print("Downloading...")
    
    for url in maincontent.findAll('a', href=True):
        
        count += 1
        
        url = url['href']
        
        
        #Excluding different urls
        if (url[0] == '/'):
        
            #Avoiding duplicated images
            if (url not in urls_array):
                
                try:
                    
                    download_url = header + url
                    file_name = "wallpaper" + str(count) +'.jpg'
                
                    with open(file_name, 'wb') as f:
                        img = scraper.get(download_url, stream=True)
                        img.raw.decode_content = True
                        shutil.copyfileobj(img.raw, f)
                        
                    #Check if Proportion filter is used
                    if (filt == "S" or filt == "s"):
                        
                        if (min_prop > -1.0 and max_prop > -1.0):
                        
                            image = Image.open(file_name)
                            width, height = image.size
                            image.close()
                            
                            if (not (min_prop < (width/height) < max_prop)):
                                os.remove(file_name)
                        
                        else:
                            print("Not acurate proportions")
                
                except Exception as e:
                    print(e)

            urls_array.append(url)
    

