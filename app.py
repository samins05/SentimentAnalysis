from transformers import pipeline
from bs4 import BeautifulSoup
import requests
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

sid_obj = SentimentIntensityAnalyzer()
total_negative = 0
total_positive = 0
reviews = [] # array of all reviews on first page



custom_headers = {
    "Accept-language": "en-GB,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
}

def get_soup(url):
    response = requests.get(url, headers=custom_headers)
    #create and return soup object to look at the html of each amazon review page
    soup = BeautifulSoup(response.text, "lxml")
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
    soup = get_soup(url)
    analyze_reviewpage(soup)
    print("Total sentiment ratio: ", get_sentimentratio())
    if(get_sentimentratio()>.60):
        print("This product is receiving positive feedback from customers!")
    elif(get_sentiment()<.40):
        print("This product is receiving negative feedback from customers :(")
    else: 
        print("Customers have mixed feeling about this product.")
def get_sentiment(review):
    #review_negative = 0 # number of sentences that are negative in the review
    #review_positive = 0 # number of sentences that are positive in the review 
    #review_neutral = 0
    global total_positive
    global total_negative
    review_sentences = review.split('.')
    for sentence in review_sentences:
        sentiment_dict = sid_obj.polarity_scores(sentence)
        if sentiment_dict['compound'] >= 0.05 :
            total_positive+=1
            #review_positive+=1

        elif sentiment_dict['compound'] <= - 0.05 :
            total_negative+=1
            #review_negative+=1
    #print('positive: ', review_positive)
    #print('negative: ', review_negative)
    #print('neutral: ', review_neutral)

def get_sentimentratio():
    return (total_positive*1.0)/(total_negative+total_positive)

#print(sentiment_info[0]["label"], ' ', sentiment_info[0]["score"])

# data = [r_content_element]
# print(sentiment_pipeline(data))

url = 'https://www.amazon.com/Bose-QuietComfort-45-Bluetooth-Canceling-Headphones/product-reviews/B098FKXT8L/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews'
analyze_reviews(url)
