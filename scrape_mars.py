# Setup and dependencies

from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # --- Mars News ---
    browser.visit('https://mars.nasa.gov/news/')
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Search for news titles and teaser paragraphs
    results = soup.find_all('ul', class_='item_list')
    
    for result in results:
        title = result.find_all('div', class_='content-title')
        paragraph = result.find_all('div', class_='article_teaser_body')

        # Extract the first title and paragraph, and assign to variables
        news_title = title[0].text
        news_paragraph = paragraph[0].text

    # --- JPL Mars Space Image - Featured Image ---
    browser.visit('https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html')
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Find image url
    image = soup.find('a', class_='showimg')['href']
    featured_image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + image

    # --- Mars Facts ---
    url = 'https://space-facts.com/mars/'

    # Use Pandas to parse the url
    facts = pd.read_html(url)

    # Set the data frame
    mars_facts = facts[0]

    # Assign the column headers
    mars_facts.columns = ['Description', 'Value']

    # Set Index to Description column without row indexing
    mars_facts.set_index('Description', inplace=True)

    # Convert table to html
    mars_facts_table = [mars_facts.to_html(classes='data table table-borderless', index=False, header=False, border=0)]

    # --- Mars Hemispheres ---
    browser.visit('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, 'html.parser')

    hemi_names = []

    hemi_names = []

    # Search for names of all 4 hemispheres
    results = soup.find_all('div', class_='collapsible results')
    hemispheres = results[0].find_all('h3')

    # Get text and store in list
    for name in hemispheres:
        hemi_names.append(name.text)

    # Click through thumbnail links
    thumbnail_results = results[0].find_all('a')
    thumbnail_links = []

    for thumbnail in thumbnail_results:
        
        if (thumbnail.img):
            thumbnail_url = 'https://astrogeology.usgs.gov/' + thumbnail['href']
            thumbnail_links.append(thumbnail_url)
    
    full_imgs = []

    # Extract image source of full-sized images
    full_imgs = []

    for url in thumbnail_links:
        browser.visit(url)
        
        html = browser.html
        soup = bs(html, 'html.parser')
        
        results = soup.find_all('img', class_='wide-image')
        relative_path = results[0]['src']
        
        img_link = 'https://astrogeology.usgs.gov/' + relative_path
        
        full_imgs.append(img_link)

    # Store as a list of dictionaries
    mars_hemi_zip = zip(hemi_names, full_imgs)

    hemisphere_image_urls = []

    for title, img in mars_hemi_zip:
        
        mars_hemi_dict = {}
        mars_hemi_dict['title'] = title
        mars_hemi_dict['img_url'] = img
        
        hemisphere_image_urls.append(mars_hemi_dict)
    
    # Store data in a dictionary
    mars_data = {
        'news_title': news_title,
        'news_paragraph': news_paragraph,
        'featured_image': featured_image_url,
        'mars_facts': mars_facts_table,
        'hemispheres': hemisphere_image_urls
    }

    # Close browser after scraping
    browser.quit()

    # Return results
    return mars_data
    



