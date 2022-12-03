#Putting it all together.

from bs4 import BeautifulSoup
import requests
from time import sleep
from random import randint
import csv

def get_url(search_term):
    """Generate a Url from a search term"""
    search_term = search_term.replace(" ","+")

    #add term query to url
    url = f"https://www.amazon.com/s?k={search_term}&ref=nb_sb_noss"

    # add page quey placeholder
    url += "&page{}"

    return url

def extract_record(item):
    """Extract and return data from a single record"""

    #description and url
    a_tag = item.h2.a
    description = a_tag.text.strip()
    url = "https://www.amazon.com/" + a_tag.get("href")

    try:
        #price
        price_parent = item.find("span","a-price")
        price = price_parent.find("span",'a-offscreen').text

    except AttributeError:
        return

    #ratings and reviews
    try:
        rating = item.i.text
    except AttributeError:
        rating = ""

    try:    
        reviews = item.find("span", "a-size-base s-underline-text").text
    except AttributeError:
        reviews = ""

    Product = (description,price, rating,reviews, url)

    return Product

# main function

def main(search_term):
    """Run main program routine"""

    records = []

    url = get_url(search_term)

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en-GB,en;q=0.5",
        "Referer":"https://www.google.com/",
        "Accept-Encoding": "gzip, deflate",
        "Dnt":"1"
        }

    for page in range(1,21):
        r = requests.get(url.format(page), headers=headers)
        soup = BeautifulSoup(r.content,"html.parser")
        result = soup.find_all("div", {"data-component-type": "s-search-result"})

        for item in result:
            record = extract_record(item)
            if record:
                records.append(record)
    sleep(randint(100,120))
    r.close()
     

    #save data file 
    with open("fragrances.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["description","price", "rating","reviews", "url"])
        writer.writerow(records)

main("Best Seller Perfume")
