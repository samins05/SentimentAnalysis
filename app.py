from textblob import TextBlob
from transformers import pipeline
from bs4 import BeautifulSoup
import requests
import pandas as pd
from transformers import pipeline

sentiment_pipeline = pipeline("sentiment-analysis")
total_negative = 0
total_positive = 0


custom_headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'accept-language': 'en-GB,en;q=0.9',
}

reviews = []

def get_soup(url,headers):
    response = requests.get(url, headers=headers)
    #create and return soup object to look at the html of each amazon review page
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


# print the text reviews of each amazon review page
def analyze_reviewpage(soup):
    #get all divs associated with each review 
    review_elements = soup.select("div.review")
    for r in review_elements:
        #store the text of the review itself in r_content_element, then append it to the reviews array
        r_content_element = r.select_one("span.review-text").text
        reviews.append(r_content_element)
        print(r_content_element)
        get_sentiment(r_content_element)

def analyze_reviews(url):   
    # go from range 1 to 30, 30 will the maximum number of pages we look at for a general idea of customers's opinions
    for x in range(1,30): 
        soup = get_soup(url,custom_headers)
        analyze_reviewpage(soup)
        # if there exists no 'next page' button on the page then stop looking for reviews, because that means there are no more reviews to look for after looking at the current page
        if soup.find('li', {'class': 'a-disabled a-last'}):
            break

def get_sentiment(review):
    review_sentences = review.split('.')
    for sentence in review_sentences:
        data = [sentence]
        sentiment_info = sentiment_pipeline(data)
        print(sentiment_info[0]["label"], ' ', sentiment_info[0]["score"])

# data = [r_content_element]
# print(sentiment_pipeline(data))

url = 'https://www.amazon.com/Bose-QuietComfort-45-Bluetooth-Canceling-Headphones/product-reviews/B098FKXT8L/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber={x}'
analyze_reviews(url)