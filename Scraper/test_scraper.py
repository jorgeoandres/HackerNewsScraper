import pytest
from hacker_news_scraper import HackerNewsScraper

def test_more_than_five_words():
    scraper = HackerNewsScraper()
    success = scraper.scrape()
    assert  min(scraper.filter_news(0,5,"comments")["num_words"]) > 5, "test failed because there are at least one element with less than 5 words"

def test_less_than_five_words():
    scraper = HackerNewsScraper()
    success = scraper.scrape()
    assert  max(scraper.filter_news(1,5,"comments")["num_words"]) <= 5, "test failed because there are at least one element that is larger than 5 words"

def test_comments_order():
    scraper = HackerNewsScraper()
    success = scraper.scrape()
    order_by_comments = scraper.filter_news(0,5,"comments")["comments"]
    assert is_ordered(order_by_comments.values.tolist()) == True, "Result is not ordered by comments"

def test_points_order():
    scraper = HackerNewsScraper()
    success = scraper.scrape()
    order_by_points = scraper.filter_news(1,5,"points")["points"]
    assert is_ordered(order_by_points.values.tolist()) == True, "Result is not ordered by points"

def is_ordered(dataframe):
    return all(dataframe[i] >= dataframe[i+1] for i in range(len(dataframe)-1))