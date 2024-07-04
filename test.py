import requests
from bs4 import BeautifulSoup
import pandas as pd

custom_headers = {
    "Accept-language": "en-GB,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
}

def get_soup(url):
    response = requests.get(url, headers=custom_headers)

    if response.status_code != 200:
        print("Error in getting webpage")
        exit(-1)

    soup = BeautifulSoup(response.text, "lxml")
    return soup

def get_reviews(soup):
    review_elements = soup.select("div.review")

    scraped_reviews = []

    for review in review_elements:
        r_content_element = review.select_one("span.review-text")
        r_content = r_content_element.text if r_content_element else None


        r = {
            "content": r_content,
        }

        scraped_reviews.append(r)

    return scraped_reviews

def main():
    search_url = "https://www.amazon.com/Bose-QuietComfort-45-Bluetooth-Canceling-Headphones/product-reviews/B098FKXT8L/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews"
    soup = get_soup(search_url)
    data = get_reviews(soup)
    df = pd.DataFrame(data=data)

    df.to_csv("amz.csv")

if __name__ == '__main__':
    main()