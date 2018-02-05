# STEP 2 - MongoDB and Flask Application
# coding: utf-8

# Dependencies
import pandas as pd
import re
import requests
import pymongo
from splinter import Browser
from bs4 import BeautifulSoup

# Create a function to execute all of your scraping code from above and
# return one Python dictionary containing all of the scraped data
def scrape ():

    # To store all data to be scraped
    marsdata = {}

    # Obtain html of Mars website
    mars_news_url = 'https://mars.nasa.gov/news/'
    mars_news_html = requests.get(mars_news_url)

    # Parse html file with BeautifulSoup
    mars_soup = BeautifulSoup(mars_news_html.text, 'html.parser')

    # Find all articles and its components
    # Need to call all classes with 'slide' to get articles on page
    articles = mars_soup.find_all('', class_='slide')

    # Create a list to store the dictionaries of article titles and paragraph texts
    # scrape_mars_data = []

    # Loop to get article titles and paragraph texts
    for result in articles:

        # Make a dictionary to store article titles and paragraph texts
        mars_title_paragraph = {}

        # Find article titles
        article = result.find('div', class_='content_title')
        title = article.find('a')
        title_text = title.text
        mars_title_paragraph['news_title'] = title_text

        # Find paragraph text
        paragraph = result.find('div', class_='rollover_description')
        # p_text = paragraph.find('div')
        p_text = paragraph.text
        mars_title_paragraph['news_p'] = p_text

        # scrape_mars_data.append(mars_title_paragraph)

        # print(title_text)
        # print(p_text)
        # print('----------')

        # Append mars_title_paragraph dictionary to main dictionary 'scrape_mars_data'
        #mars_data.append(mars_title_paragraph)
        marsdata['news_title'] = mars_title_paragraph['news_title']
        marsdata['news_p'] = mars_title_paragraph['news_p']

    # -------------------------------------
    # Create a dictionary for featured image url from JPL Mars Space Images
    mars_featured_image_dict = {}

    # Obtain html of Mars space images website
    mars_images_browser = Browser('chrome', headless=False)
    nasa_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    mars_images_browser.visit(nasa_url)

    # Parse html file with BeautifulSoup
    mars_images_html = mars_images_browser.html
    nasa_soup = BeautifulSoup(mars_images_html, 'html.parser')

    # Find image link with BeautifulSoup
    images = nasa_soup.find_all('div', class_='carousel_items')

    # Loop through images
    for nasa_image in images:
        image = nasa_image.find('article')
        background_image = image.get('style')
        
        # Use regular expression to extract url - match anything after (.)
        re_background_image = re.search("'(.+?)'", background_image)
        
        # Convert match object (url link) to string
        # group(0) includes quotations
        # group(1) gets the url link
        search_background_image = re_background_image.group(1)
        featured_image_url = f'https://www.jpl.nasa/gov{search_background_image}'

        # Add featured image url to dictionary 'mars_featured_image_dict'
        # mars_featured_image_dict['featured_image'] = featured_image_url

        # Append to featured image to main dictionary 'scrape_mars_data'
        #mars_data.append(mars_featured_image_dict)
        marsdata['featured_image'] = featured_image_url

        # print('Featured image url: ' + featured_image_url)

    # -------------------------------------
    # Create dictionary to gather all weather info from Mars weather twitter
    mars_weather_info_dict = {}

    # Get weather tweets with splinter
    twitter_browser = Browser('chrome', headless=False)
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    twitter_browser.visit(twitter_url)

    # Parse html file with BeautifulSoup
    twitter_html = twitter_browser.html
    twitter_soup = BeautifulSoup(twitter_html, 'html.parser')

    # Find weather tweets with BeautifulSoup
    mars_weather_tweets = twitter_soup.find_all('p', class_='TweetTextSize')
    mars_weather_tweets

    # Get tweets that begin with 'Sol' which indicate weather tweets
    weather_text = 'Sol '

    for tweet in mars_weather_tweets:
        if weather_text in tweet.text:
            mars_weather = tweet.text
            break
            # print(tweet.text)
            # print('----------')

            # Add tweets to dictionary 'mars_weather_info_dict'
            mars_weather_info_dict['tweet_text'] = tweet.text

            # Append to weather tweets to main dictionary 'scrape_mars_data'
            #mars_data.append(mars_weather_info_dict)
            marsdata['tweet_text'] = mars_weather_info_dict['tweet_text']

    # -------------------------------------
    # Create dictionary to gather all Mars facts
    mars_facts_dict = {}

    # Url to Mars facts website
    mars_facts_url = 'https://space-facts.com/mars/'

    # Get table from url
    mars_facts_table = pd.read_html(mars_facts_url)

    # Select table
    # mars_facts = mars_facts_table[0]

    # Add facts to dictionary 'mars_facts_dict'
    mars_facts_dict['mars_facts'] = mars_facts_table
    # print('Mars Facts:')
    # print(mars_facts_table)
    # print('----------')

    # Append to Mars facts to main dictionary 'scrape_mars_data'
    #mars_data.append(mars_weather_info_dict)
    marsdata['mars_facts'] = mars_facts_dict['mars_facts']

    # -------------------------------------
    # Create list to store dictionaries of hemisphere title and image links
    hemisphere_image_urls = []

    # Create dictionary to hold title and image url
    hemisphere_image_dict = {}

    # Use splinter to get image and title links of each hemisphere
    usgs_browser = Browser('chrome', headless=False)
    usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    usgs_browser.visit(usgs_url)

    # Parse html file with BeautifulSoup
    mars_hemispheres_html = usgs_browser.html
    mars_hemispheres_soup = BeautifulSoup(mars_hemispheres_html, 'html.parser')

    # Find hemisphere image link and title
    mars_hemispheres = mars_hemispheres_soup.find_all('div', class_='item')
    mars_hemispheres

    # Loop through each link of hemispheres on page
    for image in mars_hemispheres:
        hemisphere_url = image.find('a', class_='itemLink')
        hemisphere = hemisphere_url.get('href')
        hemisphere_link = 'https://astrogeology.usgs.gov' + hemisphere

        # Visit each link that you just found (hemisphere_link)
        usgs_browser.visit(hemisphere_link)
        
        # Need to parse html again
        mars_hemispheres_html2 = usgs_browser.html
        mars_hemispheres_soup2 = BeautifulSoup(mars_hemispheres_html2, 'html.parser')
        
        hemisphere_page = mars_hemispheres_soup2.find('img', class_='wide-image')
        hemisphere_page_src = hemisphere_page.get('src')
        
        # Get image link
        hemisphere_link_src = 'https://astrogeology.usgs.gov' + hemisphere_page_src
        
        hemisphere_title = mars_hemispheres_soup2.find('h2', class_='title')
        hemisphere_title_text = hemisphere_title.text
        
        # Append title and image urls of hemisphere to dictionary
        hemisphere_image_dict['title'] = hemisphere_title_text
        hemisphere_image_dict['img_url'] = hemisphere_link_src
        
        # Append dictionaries to list
        hemisphere_image_urls.append(hemisphere_image_dict)

        # Append to main dictionary 'scrape_mars_data'
        #mars_data.append(hemisphere_image_urls)
        marsdata['title'] = hemisphere_image_dict['title']
        marsdata['img_url'] = hemisphere_image_dict['img_url']

    print(marsdata)
    return marsdata