from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    mars_data = {}
    browser = init_browser()

    # NASA Mars News  
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)

    html = browser.html
    soup = bs(html, 'html.parser')

    # Save the latest article's title and description
    news_title = soup.find("div", class_ = "content_title").text
    news_title

    news_p = soup.find("div", class_ = "rollover_description_inner").text
    news_p

    mars_data["news_title"] = news_title
    mars_data["news_p"] = news_p

    # JPL Mars Space Images - Featured Image
    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(img_url)

    #Find the image 
    browser.find_by_id('full_image').click()
    time.sleep(3)
    browser.find_link_by_partial_text('more info').click()

    html2 = browser.html
    soup2 = bs(html2, 'html.parser')

    #Store the image path as variable 
    partial_url = soup2.select_one('figure.lede a img').get('src')
    partial_url

    featured_image_url = f'https://www.jpl.nasa.gov{partial_url}'
    featured_image_url
    mars_data["featured_image_url"] = featured_image_url

    #Mars Weather
    mars_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(mars_url)
    html3 = browser.html
    soup3 = bs(html3, 'html.parser')

    mars_weather = soup3.find("p", class_ = "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    mars_weather
    mars_data["mars_weather"] = mars_weather

    facts_url = 'https://space-facts.com/mars/'
    table = pd.read_html(facts_url)

    mars_facts = table[0]
    mars_facts.columns = ["Category", "Fact"]

    html_table = mars_facts.to_html()
    html_table
    
    mars_facts
    mars_data["mars_facts"] = html_table

    # Mars Hemispheres
    #Visit the Mars Hemispheres URL 
    mars_hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hem_url)
    html4 = browser.html
    soup4 = bs(html4, 'html.parser')

    hem_urls=[]

    for hem in range (4):
        time.sleep(2)
        images = browser.find_by_tag('h3')
        images[hem].click()
        html4 = browser.html
        soup4 = bs(html4, 'html.parser')
        partial = soup4.find("img", class_="wide-image")["src"]
        img_title = soup4.find("h2",class_="title").text
        img_url = 'https://astrogeology.usgs.gov'+ partial
        dictionary={"title":img_title,"img_url":img_url}
        hem_urls.append(dictionary)
        browser.back() 

    mars_data["hem_urls"] = hem_urls

    # Store data in a dictionary
    # mars_data = {
    #     "news_title": news_title,
    #     "news_p": news_p,
    #     "featured_image_url": featured_image_url, 
    #      "mars_weather": mars_weather,
    #      "mars_facts": mars_facts,
    #      "mars_images": hem_urls
    #  }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data

if __name__ == "__main__":
    print(scrape_info())