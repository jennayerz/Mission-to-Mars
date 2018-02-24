# STEP 2 - MongoDB and Flask Application

# Dependencies
import pandas as pd
import re
import requests
import pymongo
from splinter import Browser
from bs4 import BeautifulSoup
from flask import Flask, render_template, redirect

# Create flask app
app = Flask(__name__)

# Connect to MongoDB
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# Use database and create it
db = client.marsDB
collection = db.marsdata

# Create a function to execute all of your scraping code from above and
# return one Python dictionary containing all of the scraped data
def scrape_mars():

    # # To store all data to be scraped
    # marsdata = {}

    # # Obtain html of Mars website
    # mars_news_url = 'https://mars.nasa.gov/news/'
    # mars_news_html = requests.get(mars_news_url)

    # # Parse html file with BeautifulSoup
    # mars_soup = BeautifulSoup(mars_news_html.text, 'html.parser')

    # # Create a list to store the dictionaries of article titles and paragraph texts
    # scrape_mars_data = []

    # article_titles =  mars_soup.find_all('div', class_='content_title')

    # # To store all data to be scraped
    # marsdata = {}

    # # Obtain html of Mars website
    # mars_news_url = 'https://mars.nasa.gov/news/'
    # mars_news_html = requests.get(mars_news_url)

    # # Parse html file with BeautifulSoup
    # mars_soup = BeautifulSoup(mars_news_html.text, 'html.parser')

    # # Create a list to store the dictionaries of article titles and paragraph texts
    # scrape_mars_data = []

    # article_titles =  mars_soup.find_all('div', class_='content_title')

    # paragraph_texts = mars_soup.find_all('div', class_='rollover_description')


    for article, paragraph in zip(article_titles, paragraph_texts):

        # Make a dictionary to store article titles and paragraph texts
        mars = {}

        # Find article titles
        title = article.find('a')
        title_text = title.text
        mars['news_title'] = title_text

        # Find paragraph text
        p_text= paragraph.find('div')
        news_p = p_text.text
        mars['news_p'] = news_p
        #
        # if db.marsdata.find({<check title refer to docs>}).limit(1).size(
        print(mars)
        db.marsdata.insert(mars)
    

#     # Loop to get article titles and paragraph texts
#     for article in article_titles:

#         # Make a dictionary to store article titles and paragraph texts
#         mars_title_paragraph = {}

#         # Find article titles
#         title = article.find('a')
#         title_text = title.text
#         mars_title_paragraph['news_title'] = title_text

#         scrape_mars_data.append(mars_title_paragraph)

#     paragraph_texts = mars_soup.find_all('div', class_='rollover_description')

#     for paragraph in paragraph_texts:

#         # Make a dictionary to store article titles and paragraph texts
#         mars_title_paragraph = {}

#         # Find paragraph text
#         p_text= paragraph.find('div')
#         news_p = p_text.text
#         mars_title_paragraph['news_p'] = news_p

#         scrape_mars_data.append(mars_title_paragraph)

#     marsdata['news_data'] = scrape_mars_data

#     # -------------------------------------
#     # Obtain html of Mars space images website
#     mars_images_browser = Browser('chrome', headless=False)
#     nasa_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
#     mars_images_browser.visit(nasa_url)

#     # Parse html file with BeautifulSoup
#     mars_images_html = mars_images_browser.html
#     nasa_soup = BeautifulSoup(mars_images_html, 'html.parser')

#     # Find image link with BeautifulSoup
#     images = nasa_soup.find_all('div', class_='carousel_items')

#     # Loop through images
#     for nasa_image in images:

#         image = nasa_image.find('article')
#         background_image = image.get('style')
        
#         # Use regular expression to extract url - match anything after (.)
#         re_background_image = re.search("'(.+?)'", background_image)
        
#         # Convert match object (url link) to string
#         # group(0) includes quotations
#         # group(1) gets the url link
#         search_background_image = re_background_image.group(1)
#         featured_image_url = f'https://www.jpl.nasa/gov{search_background_image}'

#         # Append to featured image to main dictionary 'scrape_mars_data'
#         marsdata['featured_image'] = featured_image_url

#     # -------------------------------------
#     # Create list to store dictionaries of weather info
#     mars_weather_info = []

#     # Get weather tweets with splinter
#     twitter_browser = Browser('chrome', headless=False)
#     twitter_url = 'https://twitter.com/marswxreport?lang=en'
#     twitter_browser.visit(twitter_url)

#     # Parse html file with BeautifulSoup
#     twitter_html = twitter_browser.html
#     twitter_soup = BeautifulSoup(twitter_html, 'html.parser')

#     # Find weather tweets with BeautifulSoup
#     mars_weather_tweets = twitter_soup.find_all('p', class_='TweetTextSize')
#     mars_weather_tweets

#     # Get tweets that begin with 'Sol' which indicate weather tweets
#     weather_text = 'Sol '

#     for tweet in mars_weather_tweets:
#         if weather_text in tweet.text:
#             mars_weather = tweet.text

#             # Create dictionary to gather all weather info from Mars weather twitter
#             mars_weather_info_dict = {}

#             # Add tweets to dictionary 'mars_weather_info_dict'
#             mars_weather_info_dict['tweet_text'] = tweet.text

#             # Append to weather tweets to main dictionary 'scrape_mars_data'
#             mars_weather_info.append(mars_weather_info_dict)

#     marsdata['tweets'] = mars_weather_info

#     # -------------------------------------
#     # Url to Mars facts website
#     mars_facts_url = 'https://space-facts.com/mars/'

#     # Get table from url
#     mars_facts_table = pd.read_html(mars_facts_url)

#     # Select table
#     mars_facts = mars_facts_table[0]

#     mars_facts = mars_facts.to_html()

#     # Add facts to dictionary 'mars_facts_dict'
#     marsdata['mars_facts'] = mars_facts.replace('\n', '')

#     # -------------------------------------
#     # Create list to store dictionaries of hemisphere title and image links
#     hemisphere_image_urls = []

#     # Use splinter to get image and title links of each hemisphere
#     usgs_browser = Browser('chrome', headless=False)
#     usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
#     usgs_browser.visit(usgs_url)

#     # Parse html file with BeautifulSoup
#     mars_hemispheres_html = usgs_browser.html
#     mars_hemispheres_soup = BeautifulSoup(mars_hemispheres_html, 'html.parser')

#     # Find hemisphere image link and title
#     mars_hemispheres = mars_hemispheres_soup.find_all('div', class_='description')

#     # Loop through each link of hemispheres on page
#     for image in mars_hemispheres:
#         hemisphere_url = image.find('a', class_='itemLink')
#         hemisphere = hemisphere_url.get('href')
#         hemisphere_link = 'https://astrogeology.usgs.gov' + hemisphere

#         # Visit each link that you just found (hemisphere_link)
#         usgs_browser.visit(hemisphere_link)

#         # Create dictionary to hold title and image url
#         hemisphere_image_dict = {}
        
#         # Need to parse html again
#         mars_hemispheres_html = usgs_browser.html
#         mars_hemispheres_soup = BeautifulSoup(mars_hemispheres_html, 'html.parser')
        
#         hemisphere_link = mars_hemispheres_soup.find('a', text='Original').get('href')
#         hemisphere_title = mars_hemispheres_soup.find('h2', class_='title').text.replace(' Enhanced', '')
        
#         # Append title and image urls of hemisphere to dictionary
#         hemisphere_image_dict['title'] = hemisphere_title
#         hemisphere_image_dict['img_url'] = hemisphere_link

#         # Append dictionaries to list
#         hemisphere_image_urls.append(hemisphere_image_dict)

#         # Append to main dictionary 'scrape_mars_data'
#     marsdata['hemisphere_image_urls'] = hemisphere_image_urls
    
#     print(marsdata)
    return print(mars)


# # Create root/index route to query mongoDB and pass mars data to HTML template to display data
# @app.route('/')
# def index():
#     marsdata = db.marsdata.find_one()
#     return render_template('index.html', marsdata=marsdata)


# # Create route called /scrape
# @app.route('/scrape')
# def scrape():
#     data = scrape_mars()
#     # marsdata = db.marsdata.insert_many(data)
#     db.marsdata.update(
#         {},
#         data,
#         upsert=True
#     )
#     return "Scraping successful!"

if __name__ == '__main__':
    app.run(debug=True)
    scrape_mars()