import pandas as pd
import requests
from bs4 import BeautifulSoup
import time


def getsoup(url):
    """
    Given a url to the first page of Amazon product reviews,
    create a soup object linked to that url.

    Args:
        url: A string that is the url to the 'All Reviews' page
        of an Amazon product.

    Returns:
        soup = A BeautifulSoup object that is linked to the 'All Reviews'
        page of an Amazon product.
    """
    # using a header that will allow us to access Amazon's review pages
    header = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
    response = requests.get(url, headers={'User-Agent': header})
    status_code = response.status_code

    # checking to see that the website works and otherwise
    # running the function again till it does
    if status_code == 200:
        soup = BeautifulSoup(response.content)
    else:
        soup = getsoup(url)
    return soup


def getsoupdata(url):
    """
    Function to repeatedly get the soup object from the input URL
    until useful data is returned.

    Args:
        url: A string that is the url to the 'All Reviews' page
        of an Amazon product.

    Returns:
        soup = A BeautifulSoup object that is linked to the
        'All Reviews' page of an Amazon product.
    """
    soup = getsoup(url)
    # keep getting soup object as long as access to data is blocked by Amazon
    while "To discuss automated access to Amazon data" in str(soup):
        soup = getsoup(url)
        time.sleep(0.1)
    return soup


def find_last_page(soup):
    """
    Given a soup object that contains the HTML structure of an Amazon
    reviews page, find the index of the last page of reviews.

    Args:
        soup: A BeautifulSoup soup object that is linked to the 'All Reviews'
        page of an Amazon product.

    Returns:
        last_page: An integer that is the index of the last page of reviews.
    """
    html = str(soup.prettify())
    # The total number of reviews for an Amazon product is found
    # before the string 'global reviews' in HTML code
    index = html.find('global reviews')
    num_of_reviews = html[index - 5: index - 1]
    # filtering other characters except for the number that represents
    # the total number of reviews
    numeric_filter = filter(str.isdigit, num_of_reviews)
    numeric_string = "".join(numeric_filter)
    num_of_reviews = int(numeric_string)
    # This math gives us the index of the last page of reviews
    # because there are a total of 10 reviews per page
    last_page = num_of_reviews // 10 + 1
    return last_page


def find_urls(last_page, url):
    """
    Find the url for each page of reviews for an Amazon product.

    Args:
        last_page: A number that is the index of the last page of reviews.
        url: A string that is the url to the 'All Reviews' page of an
        Amazon product.

    Returns:
        reviews_url_list: A list that contains the url of every page of
        reviews for an Amazon product.
    """
    reviews_url_list = [url]
    # To access the subsequent review pages, the string &pageNumber +
    # page number has to be added at the end of the original link
    for page_number in range(2, last_page):
        reviews_url_list.append(url + "&pageNumber=" + str(page_number))
    return reviews_url_list


def get_reviews(soup, url):
    """
    Given a soup object and url to a page of Amazon product reviews,
    access the all reviews on that page and load them into a dataframe.

    Args:
        soup: A BeautifulSoup soup object that is linked to the 'All Reviews'
        page of an Amazon product.
        url: A string that is the url to the 'All Reviews' page of
        an Amazon product.

    Returns:
        df = A dataframe containing all reviews on that reviews page of an
        Amazon product.
    """
    soup = getsoupdata(url)
    # extracting the raw text of the reviews
    review_text_sec = soup.find_all("span", 'a-size-base review-text \
    review-text-content')
    text = []
    for t in review_text_sec:
        text.append(t.text[4:-2])

    # Creating a dataFrame out of all the required elements of the review page
    da = {'Review_text': text}
    df = pd.DataFrame.from_dict(da, orient='index')
    df = df.transpose()
    return df


def get_all_reviews_for_one(url):
    """
    Given a url to the first page of Amazon product reviews,
    access all reviews on that page and all pages following.

    Args:
        url: A string that is the url to the 'All Reviews' page of
        an Amazon product.

    Returns:
        df: A Pandas dataframe that contains all reviews of the product
        linked to the input url. This dataframe has one column header,
        'Review_text', with an individual review to each row.
    """

    # creating a list of all the urls for one coffee
    soup = getsoupdata(url)
    last_page = find_last_page(soup)
    url_list = find_urls(last_page, url)
    df1 = pd.DataFrame(columns=['Review_text'])
    # getting all the reviews from every page of reviews from Amazon
    # and appending it to a dataframe.
    for url in url_list:
        df = get_reviews(soup, url)
        df1 = df1.append(df, ignore_index=True)
    return df1
