#!/usr/bin/env python
# coding: utf-8

# ## Scraping

# In[1]:


# Dependencies & Set-up
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# ### NASA Mars News

# In[2]:


# Set-up splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Set URL
browser.visit('https://mars.nasa.gov/news/')

html = browser.html
soup = bs(html, 'html.parser')


# In[3]:


# Search for news titles and teaser paragraphs
results = soup.find_all('ul', class_='item_list')

# Loop through results
for result in results:
    
    title = result.find_all('div', class_='content_title')
    paragraph = result.find_all('div', class_='article_teaser_body')
    
    # Extract the first title and paragraph, and assign to variables
    news_title = title[0].text
    news_paragraph = paragraph[0].text
    


# ### JPL Mars Space Images - Featured Image

# In[4]:


# Open browser to JPL Featured Image

# Set URL
browser.visit('https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html')

html = browser.html
soup = bs(html, 'html.parser')


# In[5]:


# Find image relative path
image = soup.find('a', class_='showimg')['href']
print(image)


# In[6]:


# Add relative path to full URL string
featured_image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + image
print(featured_image_url)


# ### Mars Facts

# In[7]:


# Establish Mars facts url
url = 'https://space-facts.com/mars/'

# Use Pandas to parse the url
facts = pd.read_html(url)

# Set the data frame
mars_facts = facts[0]

# Assign the column headers
mars_facts.columns = ['Description', 'Value']

# Set Index to Description column without row indexing
mars_facts.set_index('Description', inplace=True)

# Display
mars_facts


# In[8]:


# Convert to html

mars_facts_table = [mars_facts.to_html(classes='data table table-borderless', index=False, header=False, border=0)]
mars_facts_table


# ### Mars Hemispheres

# In[9]:


# Open browser to USGS Astrogeology site
browser.visit('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')


# In[10]:


# Set up
html = browser.html
soup = bs(html, 'html.parser')

hemi_names = []

# Search for names of all 4 hemispheres
results = soup.find_all('div', class_='collapsible results')
hemispheres = results[0].find_all('h3')

# Get text and store in list
for name in hemispheres:
    hemi_names.append(name.text)
    
hemi_names


# In[11]:


# Click through thumbnail links
thumbnail_results = results[0].find_all('a')
thumbnail_links = []

for thumbnail in thumbnail_results:
    
    if (thumbnail.img):
        thumbnail_url = 'https://astrogeology.usgs.gov/' + thumbnail['href']
        thumbnail_links.append(thumbnail_url)

thumbnail_links      


# In[12]:


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

full_imgs


# In[13]:


# Store as a list of dictionaries

mars_hemi_zip = zip(hemi_names, full_imgs)

hemisphere_image_urls = []

for title, img in mars_hemi_zip:
    
    mars_hemi_dict = {}
    mars_hemi_dict['title'] = title
    mars_hemi_dict['img_url'] = img
    
    hemisphere_image_urls.append(mars_hemi_dict)

hemisphere_image_urls


# In[14]:


browser.quit()


# In[ ]:




