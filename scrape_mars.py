from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time


def scrape():
    # Using splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # URL of page to be scraped

    mars_news_url = "https://redplanetscience.com"

    browser.visit(mars_news_url)

    time.sleep(1)

    html = browser.html

    # Create BeautifulSoup object; parse with 'html parser'

    soup = BeautifulSoup(html, 'html.parser')

    # Retrieve article title and paragraph text

    result = soup.find('div', class_="list_text")

    title_mars = result.find('div', class_="content_title").get_text()
    para_text = result.find('div', class_="article_teaser_body").get_text()

    # close the browser

    browser.quit()

    # Using splinter

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # URL of page to be scraped

    mars_image_url = 'https://spaceimages-mars.com/'

    browser.visit(mars_image_url)

    time.sleep(1)

    html = browser.html

    # Create BeautifulSoup object; parse with 'html parser'

    soup = BeautifulSoup(html, 'html.parser')

    # Retrieve image link

    result = soup.find_all('a', class_='showimg')[0]['href']

    featured_image_url = 'https://spaceimages-mars.com/' + result

    # pandas read html tables

    mars_fact_url = 'https://galaxyfacts-mars.com/'

    # use pandas to scrape table and store as a data frame

    df_mars_facts = pd.read_html(mars_fact_url)[0]

    # Rename the columns

    df_mars_facts.columns = ['Description', 'Mars', 'Earth']

    df_mars_facts.drop(df_mars_facts.index[:1], inplace=True)

    # Setting new index

    df_mars_facts.set_index('Description', inplace=True)

    # conveting to html table

    html_table = df_mars_facts.to_html()
    html_table.replace('\n', '')

    # table html

    mars_table = df_mars_facts.to_html()

    # Using splinter

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # URL of page to be scraped

    url = 'https://marshemispheres.com/'
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    # get the list of image headings

    mars_hemispheres = []
    links = soup.find_all('h3')

    for link in links:
        # print(hemi.text)
        mars_hemispheres.append(link.text)

    mars_hemi = mars_hemispheres[0:4]

    hemisphere_image_urls = []
    data = {}

    for title in mars_hemi:

        browser.click_link_by_partial_text(title)

        data = {
            'title': title,
            'image': browser.links.find_by_partial_text('Sample')['href']
        }

        # print(data)

        hemisphere_image_urls.append(data)

        browser.back()

     # Store all scraped data in a dictionary
    mars_data = {
        "news_title": title_mars,
        "Text": para_text,
        "featured_image_url": featured_image_url,
        "mars_table": mars_table,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
