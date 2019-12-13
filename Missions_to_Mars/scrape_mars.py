from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    # NASA Mars News  
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)

    html = browser.html
    soup = bs(html, 'html.parser')

    try: 
        news_title = soup.find("div", class_="content_title").find("a").get_text()
        news_p = soup.find("div", class_="article_teaser_body").get_text()
    except: 
        news_title = 'Latest headline could not be found'
        news_p = ''
        print('News error')
    
        news_title
        news_p

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

    #Mars Weather
    mars_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(mars_url)
    html3 = browser.html
    soup3 = bs(html3, 'html.parser')

    mars_weather = soup3.find("p", class_ = "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    mars_weather

    facts_url = 'https://space-facts.com/mars/'
    table = pd.read_html(facts_url)

    mars_facts = table[0]
    mars_facts.columns = ["Category", "Fact"]

    mars_facts

    html_table = mars_facts.to_html()
    html_table

    # Mars Hemispheres
    #Visit the Mars Hemispheres URL - New link(Original link is not working)
    mars_hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hem_url)
    html4 = browser.html
    soup4 = bs(html4, 'html.parser')

    hemispheres = soup4.find_all('div', class_="full-content")

    hem_title = soup4.find('div', class_="item").find('h3').text
    hem_title

    hem_img = soup4.find('div', class_="item").find('a').get('href')
    hem_img

    hem_url = 'https://astrogeology.usgs.gov/'
    print(f'https://astrogeology.usgs.gov/'+hem_img)

    hemispheres=soup4.find_all('div', class_="item")

    #Loops through site for image and links 
    hem_urls=[]

    for hemisphere in hemispheres:
        #hemisphere_dict = {}
        hem_title = hemisphere.find('a').find('img').get('alt')
        hem_img_temp = hemisphere.find('a').get('href')
        hem_img = f'https://www.jpl.nasa.gov{hem_img_temp}'
        hem_urls.append({'title':hem_title,'img_urls':hem_img})
        #print(hem_title, hem_img)
    hem_urls


    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url, 
        "mars_weather": mars_weather
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data

if __name__ == "__main__":
    print(scrape())
