from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from fake_useragent import UserAgent
import time
import random
from selenium.webdriver.chrome.options import Options
import pymysql
import pymysql.cursors

#These are links to try and scan all going to the same McDonald's
FuboTV = ("https://www.fubo.tv/welcome")
Sports_Aggregator = ('https://sports-aggregator.circuitbreakers.tech')
Peacock =('https://www.peacocktv.com/')
ABC = ("https://abc.com/")
Disney_plus = ("https://www.disneyplus.com/")
ESPN = ("https://www.espn.com/")
# result = requests.get(url).text

# Dont delete commented code here since this was done to try and fool the anti-bot at grubhub.
# options = Options()
# ua = UserAgent()
# user_agent = ua.random
# print(user_agent)
# options.add_argument(f'--user-agent={user_agent}')
# driver = webdriver.Chrome(options=options)

# Driver is from a module called Selenium that you are going to need to install (pip3 install selenium). Selenium is used to have beautifulsoup4
# read javascript because if you do it normally it won't work.

# This code is to tell the webdriver from selenium what browser to use. For example its using Chrome.
driver = webdriver.Chrome()
# driver.get is to tell the webdriver to what website to search and scan.
driver.get(FuboTV)
driver.get(ABC)
driver.get(ESPN)
driver.get(Disney_plus)
driver.get(Peacock)

# x and l are variables used in order to control the while loop statement thats used below, for example l its used as the limit of iterations
# while x counts the amounts of iterations.(Right now its on 50 for testing purposes. Recommend to put it on 600 for an actual scan).
x = 0
l = 50

# The variable divs its being used to store all the data that is gathered by beautifulsoup4 in order to use later in an for loop.
divs = []

while True:
    x += 1
    # driver.execute is being used here to scroll very slowly through the website and heavly recommend to leave it at 30 since the data on
    # the websites clear very fast while scrolling and 30 seems to be catching everything so far.
    driver.execute_script('scrollBy(0,30)')
    # page variable is just telling beautifulsoup4 where to read the website and also the encoder.
    page = BeautifulSoup(driver.page_source, 'lxml')
    # In the results variable is set to save the page.findAll expression which what it does is that it searches the page variable based on
    # the requirements that you give it, for example here the requirements is that the tag must be a div and the data anchor id to be
    # MenuItem. findAll what it does is that it searches the entire document while find only searches for the first one.
    results = page.findAll('div', {'data-anchor-id' : "sites"})
    # .extend saves all input to the divs variable from before the while loop.
    divs.extend(results)
    print(f'{x} of {l} done.')

    # this segment of code here is to print the content in a html file for testing purposes.
    # with open('dd.html', 'w', encoding='utf-8') as f:
    #     f.write(str(page.contents))
    # n = random.randint(0,50)
    # if n == 5:
    #     print('Time to sleep')
    #     time.sleep(2)
    
    # This can most likely be ignored since its just to increase the limit on the l variable by 200 iterations if you are running different pages.
    # if x == l:
    #     j = input('Do you want to add more? (Y/N)')
    #     if j == 'Y':
    #         l+=200
    #     else:
    #         break

    if x == l:
        break

# db_link is just for the connection and a print statement so please just change it here.
db_link = '10.100.33.60'

connection = pymysql.connect(
    database = 'sports_aggregator',
    user = 'svassell2',
    password = '228426979',
    host = db_link,
    cursorclass = pymysql.cursors.DictCursor
)

# limit variable and the if statement are just a failed attempt at stopping the code from replicating data by having it check if the data already exist.
limit = []
for users in divs:
    limit.extend(users)
    if users in limit:
        continue
    else:
        # the next for segments are using the .find from beautifulsoup as explained before to try and filter out the items by using a attribute unique for them.
        # .contents is used to only gather the actual text and not the code with text.
        Item_Name = users.find('h3', {'data-telemetry-id' : "sites"})
        sites_name = Item_Name.contents

        Price = users.find('span', {'data-anchor-id' : "sites"})
        item_price = Price.contents
        item_price = [item.replace('$', '') for item in item_price]

        Picture = users.find('img')
        item_picture = Picture.attrs['src']

        Des = users.find('span', {'data-telemetry-id' : "sites"})
        item_des = Des.contents

        cursor = connection.cursor()
        # this code is to make the bot automatically upload the data into the database. For now its manual input on restaurant and category but hopefully we could get the category automated.
        cursor.execute(f'INSERT INTO `sites` (`sites, `teams`, `leagues`, `streaming`, `user`) VALUES ("{sites_name[0]}", "{item_picture}", "1", "{item_des[0]}", "1");')
        connection.commit()
        # this execute is to be able to get the id of the item uploaded to be able to assign the id on the price.
        cursor.execute(f"SELECT `leagues` FROM `sites` ORDER BY `user_id` DESC;")
        connection.commit()
        id = cursor.fetchone()
        result = id['user_id']
        # this execute uploads the price and also uses the id collected before in order to connect it with the item.
        cursor.execute(f'INSERT INTO `sites` (`price_value`, `item_id`, `service_id`) VALUES ("{item_price[0]}", "{result}","1")')
        cursor.close()
        connection.commit()

print(f'Data has been submitted to the Database. Please check if data is correct on: {db_link}')

driver.quit()