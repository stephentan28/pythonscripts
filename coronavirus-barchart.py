import time
import re
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

# driver = webdriver.Chrome(ChromeDriverManager().install())
PATH    = "/Users/steph/.wdm/drivers/chromedriver/81.0.4044.138/win32/chromedriver"

# Define URL
URL = "https://www.worldometers.info/coronavirus/countries-where-coronavirus-has-spread/"

browser = webdriver.Chrome(PATH)
browser.get(URL)
    
# Give the browser time to load all content.
time.sleep(3)

countryCases = {}

for page in range(0,2):

    content = browser.find_elements_by_css_selector("#table3")
    for e in content:   
        textContent  = e.get_attribute('innerHTML')
        # Beautiful soup removes HTML tags from our content if it exists.
        soup         = BeautifulSoup(textContent, features="lxml")
    
        # Create a string delimiter with a unique character combination.
        content      = soup.get_text(separator='??') 
        contentList  = content.split("??")
        
        newList = []
        for i in range(0,len(contentList)):
            tempString = contentList[i]
            tempString = tempString.strip() # Remove leading and trailing spaces.
            tempString = re.sub(r"[\n\t]*", "", tempString)
        
            # Remove 2+ consecutive spaces.
            tempPhrase = re.sub('[ ]{2,}', '*', tempString)

            # Removes other special characters.
            tempPhrase = tempPhrase.encode('ascii', 'ignore').decode('ascii')
    
            if(len(tempPhrase)>1):
                newList.append(tempPhrase)
        #print(newList)

# Add Country, Cases, Deaths and Region to Dictionary
countryCases.update(
        {
        'Country' : newList[4::4],
        'Cases' : newList[5::4],
        'Deaths' : newList[6::4],        
        'Region' : newList[7::4]        
        }
        )    

# Create a Dataframe
df = pd.DataFrame(countryCases)

# Create a Dataframe selecting top 10 only
df2 = df.loc[0:9]
df2['Cases'] = df2['Cases'].str.replace(',','').astype(int)
df2['Deaths'] = df2['Deaths'].str.replace(',','').astype(int)

# Create plot of Cases and Deaths by Country
ax = df2.plot(x='Country', y=['Cases','Deaths'], title = 'Coronavirus Cases & Deaths - Top 10', kind='bar')

# Add text showing Total Cases
ax.text(0.5,0.5,"Total Cases: " + str(df2['Cases'].sum(axis=0)), horizontalalignment='center', verticalalignment='center', transform= ax.transAxes)

# Show plot
plt.show()