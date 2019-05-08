# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return( Browser("chrome", **executable_path, headless=False) )

def scrape():
    
    result = dict()
    browser = init_browser()
    
    #NASA Mars News
    url="https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')
    
    result["news_title"] = soup.find('div', class_='content_title').a.text
    result["news_p"] = soup.find('div', class_='article_teaser_body').text
    result["news_date"] = soup.find('div', class_='list_date').text
    
    #JPL Mars Space Images
    JPL_url="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(JPL_url)
    JPL_html = browser.html
    soup = BeautifulSoup(JPL_html,'html.parser')
    
    short_link = soup.find('a', class_='button fancybox')["data-fancybox-href"]
    result["featured_image_url"] = "https://www.jpl.nasa.gov"+short_link
    
    #Mars Weather
    url="https://twitter.com/marswxreport?lang=en"
    weather_html = urlopen(url)
    weather_soup = BeautifulSoup(weather_html, 'lxml')
    
    weather = weather_soup.find("p",class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    mars_weather = weather.text
    extra_text = weather.a.text
    mars_weather = mars_weather[:(len(mars_weather)-len(extra_text))]
    result["mars_weather"] = mars_weather.replace("\n"," ")
        
    #Mars Facts
    facts_url = "https://space-facts.com/mars/"
    facts_list = pd.read_html(facts_url)
    facts_table = facts_list[0]
    facts_table.columns = ["Description","Facts"]
    facts_table.set_index('Description', inplace=True)
    
    html_facts_table = facts_table.to_html()
    html_facts_table = html_facts_table.replace('\n', '')
    result["html_facts_table"] = html_facts_table
    
    
    #Mars Hemispheres
    Hemi_url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(Hemi_url)
    Hemi_html = browser.html
    soup = BeautifulSoup(Hemi_html,'html.parser')
    
    products = soup.find_all('div', class_='item')
    Hemi_main_link = "https://astrogeology.usgs.gov"
    hemisphere_image_urls = []
    
    for product in products :
        product_link = Hemi_main_link + product.a["href"]
        product_dict = dict()
        try:
            browser.visit(product_link)
            product_html = browser.html
            product_soup = BeautifulSoup(product_html,'html.parser')
        
            product_dict["title"] = product_soup.find('div', class_='content').h2.text
        
            short_img_link = product_soup.find('img', class_='wide-image')["src"]
            product_dict["img_url"] = Hemi_main_link + short_img_link
        
            hemisphere_image_urls.append(product_dict)
        except :
            print("Your URL gets wrong.")
    
    result["hemisphere_image_urls"] = hemisphere_image_urls 
    
    #create a scrape_time to store scraping time
    result["scrape_time"] = str(datetime.datetime.now())
    
    browser.quit()
    
    return(result)
    
    