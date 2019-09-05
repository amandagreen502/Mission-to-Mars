from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

# https://splinter.readthedocs.io/en/latest/drivers/chrome.html
# !which chromedriver


def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)



def scrape_info():
    browser = init_browser()

    # Establish Nasa news url
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')
    # Examine the results, then determine element that contains sought info
    print(soup.prettify())

    # Get & Print Title and News Paragraph
    news_title = soup.find('div', class_='content_title').find('a').text
    news_p = soup.find('div', class_='rollover_description_inner').text

    # Display scrapped data 
    print(news_title)
    print(news_p)

    # Visit Mars Space Images
    url_image = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_image)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(browser.html, 'html.parser')

    # Grab Picture URL
    picture = soup.find("article", class_="carousel_item")["style"]
    # Display scrapped data 
    print(picture)

    # Clean Picture URL:
    jpeg_file = picture.split("'")[1]
    jpeg_file

    # Add to URL
    JPL_Mars_Site = "https://www.jpl.nasa.gov"
    featured_img_url = JPL_Mars_Site + jpeg_file
    featured_img_url

    # Visit Mars Twitter:
    Twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(Twitter_url)

    # Retrieve page with the requests module
    response = requests.get(Twitter_url)
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')
    # Examine the results, then determine element that contains sought info
    print(soup.prettify())

    latest_tweet = soup.find_all('div', class_='js-tweet-text-container')
    print(latest_tweet)

    for tweet in latest_tweet: 
        weather_tweet = tweet.find('p').text
        if 'Sol' and 'pressure' in weather_tweet:
            print(weather_tweet)
            break

    # Visit Mars facts url 
    facts_url = 'https://space-facts.com/mars/'

    # Use Panda's `read_html` to parse the url
    mars_facts = pd.read_html(facts_url)
    mars_facts
    # Find the mars facts DataFrame in the list of DataFrames as assign it to `mars_df`
    mars_df = mars_facts[1]


    mars_df_html = mars_df.to_html()

    # Display mars_df
    print(mars_df)

    # Visit Mars Space Images
    url_Hemispheres = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_Hemispheres)

    # Retrieve page with the requests module
    response = requests.get(url_Hemispheres)
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')
    # Examine the results, then determine element that contains sought info
    print(soup.prettify())

    item = soup.find_all("div", class_="item")
    print(item)

    base_url = 'https://astrogeology.usgs.gov/'
    browser.visit(url_Hemispheres)
    html = browser.html
    soup = bs(html, 'html.parser')
        
    hemisphere_image_urls = []

    links = soup.find_all("div", class_="item")
    for link in links:
        img_dict = {}
        title = link.find("h3").text
        next_link = link.find("div", class_="description").a["href"]
        print(url_Hemispheres)
        full_next_link = base_url + next_link
        
        browser.visit(full_next_link)
        print(full_next_link)
        
        pic_html = browser.html
        pic_soup = bs(pic_html, 'html.parser')
        
        url = pic_soup.find("img", class_="wide-image")["src"]

        img_dict["title"] = title
        img_dict["img_url"] = base_url + url
 
        
        hemisphere_image_urls.append(img_dict)
    hemisphere_image_urls

    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_img_url": featured_img_url,
        "weather_tweet": weather_tweet,
        "mars_df_html": mars_df_html,
        "hemisphere_image_urls": hemisphere_image_urls
        }

    # Close the browser after scraping
    browser.quit()

    # Return result
    return mars_data
