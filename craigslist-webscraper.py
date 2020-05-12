import time
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd

# driver = webdriver.Chrome(ChromeDriverManager().install())
PATH    = "/Users/steph/.wdm/drivers/chromedriver/81.0.4044.138/win32/chromedriver"

# Define URL and search term
URL = "https://vancouver.craigslist.org/"
SEARCH_TERM = "guitar"

# Define CSV pathway and filename
CSV_PATH = "/Users/steph/Desktop/"
CSV_FILE = 'craigslistexport_' + SEARCH_TERM + '.csv'

browser = webdriver.Chrome(PATH)
browser.get(URL)

# Define Posting class
class Posting:
    postDate = ""
    postTitle = ""
    postPrice = ""
    postLocation = ""
    
    def __init__(self, postDate, postTitle, postPrice, postLocation):
        self.postDate = postDate
        self.postTitle = postTitle
        self.postPrice = postPrice
        self.postLocation = postLocation 

    def showDetail(self):
        print("Date:     " + str(self.postDate))
        print("Title:     " + str(self.postTitle))
        print("Price:     " + str(self.postPrice))
        print("Location: " + str(self.postLocation))
        print("***")
    
# Give the browser time to load all content.
time.sleep(3)

# Find the search input.
search  = browser.find_element_by_css_selector("#query")                                        
search.send_keys(SEARCH_TERM, Keys.ENTER)

postList = []
postDict = []

for page in range(0,2):

    content = browser.find_elements_by_css_selector(".result-info")
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
            # Remove brackets
            tempPhrase = re.sub('[(|)]', "", tempString) 
            # Removes other special characters.
            tempPhrase = tempPhrase.encode('ascii', 'ignore').decode('ascii')
    
            if(len(tempPhrase)>1):
                newList.append(tempPhrase)
        #print(newList)

        POST_DATE = 1
        POST_TITLE = 2
        POST_PRICE = 3
        POST_LOCATION = 4
        
        post = Posting(newList[POST_DATE], newList[POST_TITLE], newList[POST_PRICE], newList[POST_LOCATION])
        postList.append(post)

        postDict.append(
                {
                'Date' : newList[POST_DATE],
                'Title' : newList[POST_TITLE],
                'Price' : newList[POST_PRICE],        
                'Location' : newList[POST_LOCATION]        
                }
                )

    try:
        nextPage  = browser.find_element_by_css_selector(".next")                                        
        nextPage.click()        
    except:
        print("Craigslist search completed")

# Show post detail from postList
for post in postList:
    post.showDetail()

# Create dataframe and export to CSV
dfOut = pd.DataFrame(postDict)
dfOut.to_csv(CSV_PATH + CSV_FILE, index=False)

# Display first two rows and last two rows in a new dataframe
dfSearch = dfOut
print(dfSearch.head(2))
print(dfSearch.tail(2))