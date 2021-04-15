import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager


def scrape_info():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit desplanetscience website
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the news
    news_title = soup.find(class_='content_title').text
    news_p = soup.find('div', class_= 'article_teaser_body').text
    
    #Visit the url for the Featured Space Image site
    image_url = 'https://spaceimages-mars.com/'
    browser.visit(image_url)
    time.sleep(4)
    #Use splinter to navigate the site and find the image url
    # HTML object
    imgs_html=browser.html

    soup = bs(imgs_html, 'html.parser')

    # set path for featured image url
    relative_image_path = soup.find('img', class_='headerimage fade-in')["src"]

    feature_img = image_url + relative_image_path

    #Mars Facts
    #Visit the url for the space facts webpage
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)

    # Use pandas to convert the data to a HTML table string
    tables = pd.read_html(facts_url)
    df = tables[0]
    df.columns = ['Description','Value']
    mars_df = df.set_index('Description')
    mars_facts = mars_df.to_html(index=True, header=False)

    #Mars Hemispheres
    #Visit the url for the Mars Hemisphere site 
    hemispheres_url = 'https://marshemispheres.com/'
    browser.visit(hemispheres_url)

    # HTML object
    html_hemispheres = browser.html

    #Scrape page into soup
    soup = bs(html_hemispheres, 'html.parser')
    images = soup.find_all('div', class_='item')

    # Create empty list for hemisphere urls 
    hemisphere_image_urls=[]
    for hemisphere in images: 
        # Save each hemisphere title 
        title = hemisphere.find('h3').text
        
        # Save the url string for the full resolution image of each hemisphere
        image_url = hemisphere.find('a', class_='itemLink product-item')['href']
        
        # visit the full image url for each hemisphere
        browser.visit(hemispheres_url + image_url)
        
        # HTML Object for each hemisphere full image url
        image_html = browser.html
        
        # Parsing HTML for each hemisphere full image url
        soup = bs(image_html, 'html.parser')
        
        # build full image url 
        full_image = hemispheres_url + soup.find('img', class_='wide-image')['src']
        
        # Append the dictionary with the image url string and the hemisphere title to a list
        hemisphere_image_urls.append({"title" : title, "img_url" : full_image})

    # Store data in a dictionary
    mars_data = {
        "feature_img": feature_img,
        "news_title": news_title,
        "news_p": news_p,
        "mars_fact": mars_facts,
        "mars_hemispheres": hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
