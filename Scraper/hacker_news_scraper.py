import requests
import re
import pandas as pd
from single_entry import SingleEntry
from bs4 import BeautifulSoup, SoupStrainer

class HackerNewsScraper:
  """
    Scraper for HackerNews. Functions for request, get and filter information are implemented.
  """

  MAX_ENTRIES = 30

  def __init__(self, url = "https://news.ycombinator.com/"):
    """
    Construct a new 'HackerNewsScraper' object.

    :param url: Path of the file to be scraped. In case of test you can use html file of HackerNews. Default value HackerNews webpage.
    :type url: str
    :return: returns nothing
    """
    self.URL = url
    self.content = ""
    self.news = []

  def do_request(self):
    """
    Do the http request
    :return: HTTP Response content
    :rtype: requests.Response
    """
    hacker_news_request = requests.get(self.URL)
    return hacker_news_request.content

  def get_columns_titles_and_ranks(self, objects):
    """
    Select titles and rank columns from the previous filtered '<td>' objects of the page 
    :param objects: '<td>' objects of HackerNews content
    :type objects: BeautifulSoup
    :return: HTTP Response content
    :rtype: requests.Response
    """
    columns_class_title = objects.find_all("td", attrs={"class":"title"})
    columns_ranks = objects.find_all("td", attrs={"class":"title", "align":"right"})
    columns_titles = [column for column in columns_class_title if column not in columns_ranks]
    return columns_ranks, columns_titles

  def get_columns_metrics_and_comments(self, objects):
    """
    Select metrics columns from the previous filtered '<td>' objects of the page 
    :param objects: '<td>' objects of HackerNews content
    :type objects: BeautifulSoup
    :return: HTTP Response content
    :rtype: requests.Response
    """
     columns_metrics = objects.find_all("td", attrs={"class":"subtext"})
     return columns_metrics

  def get_content_of_columns(self, columns_ranks, columns_titles, columns_metrics):
    """
    Iterate over rank, title and metrics objects to extract information
    :param columns_ranks: '<td>' objects of ranks content
    :type columns_ranks: ResultSet
    :param columns_titles: '<td>' objects of titles content
    :type columns_titles: ResultSet
    :param columns_metrics: '<td>' objects of metrics content
    :type columns_metrics: ResultSet
    :return: HTTP Response content
    :rtype: list(SingleEntry)
    """
    entries = []
    size = len(columns_ranks)
    for index in range(0,size):
      entry = SingleEntry()
      entry.rank = self.get_text(columns_ranks[index].find("span", attrs={"class":"rank"}))
      entry.title = self.get_text(columns_titles[index].find("a", attrs={"class":"storylink"}))
      entry.num_words = len(entry.title.split())
      entry.points =  self.sanitize_points(self.get_text(columns_metrics[index].find("span", attrs={"class":"score"})))
      entry.comments =  self.sanitize_comments(self.look_for_metrics(columns_metrics[index].select("a[href*=item]")))
      entries.append(entry)

    return entries

  def get_text(self,soup_object):
    """
    Extracts text of Soup Object
    :param soup_object: Object to get text
    :return: text of the object
    :rtype: str
    """
    if soup_object is None:
      return "NULL"
    else:
      return soup_object.text

  def sanitize_points(self,text):
    return self.convert_to_int("point",text.replace(" points",""))

  def sanitize_comments(self,text):
    return self.convert_to_int("comment",text.replace("\xa0comment","").replace("s",""))

  def look_for_metrics(self, metrics):
    """
    Search for the second child in metrics object. If there is not object metrics it returns empty string 
    :param metrics: Object to get text
    :return: text of the object
    :rtype: str
    """
    if len(metrics) > 1:
      return self.get_text(metrics[1])
    else:
      return ""

  def convert_to_int(self, type_text, text):
    try:
      number = int(text)
    except Exception as err:
      number = -1
      print(err.__str__())
      print(str(type_text)+" "+str(text)+" does not contain anything convertible to int, the "+str(type_text)+" will be -1")

    return number

  def scrape(self):
    hacker_news_content = self.do_request()
    td_parser = SoupStrainer("td")
    td_objects = BeautifulSoup(hacker_news_content, "html.parser", parse_only = td_parser)
    columns_ranks, columns_titles = self.get_columns_titles_and_ranks(td_objects)
    columns_metrics = self.get_columns_metrics_and_comments(td_objects)
    
    self.news = self.get_content_of_columns(columns_ranks,columns_titles, columns_metrics)
    if len(self.news) == self.MAX_ENTRIES:
      return True
    else:
      return False

  def to_dataframe(self):
    return pd.DataFrame([entry.__str__() for entry in self.news])

  def filter_news(self, comparison_type = 1, limit_of_words = 5 , ordered_by = "comments", ascending = False):
    """
    Uses a Pandas dataframe representation of the entries to filter the information
    :param comparison_type: 0 more than, 1 less than or equal
    :type comparison_type: int
    :param limit_of_words: threshold of words used to filter the dataset
    :type limit_of_words: int
    :param ordered_by: name of column to be used
    :type ordered_by: str
    :param ascending: Control the direction of the order
    :type ascending: bool
    :return: filtered test
    :rtype: pd.DataFrame
    """
    dataframe =  self.to_dataframe()
    
    if comparison_type not in [0,1]:
      raise Exception("Sorry, you can only filter the limit of words: 0 = more than, 1 = less than or equal.")
    if not isinstance(limit_of_words, int):
      raise Exception("Sorry, limit_of_words can only be integer.")
    if ordered_by not in dataframe.columns:
      raise Exception("Sorry, you can only order the filtered table by "+dataframe.columns)
    if not isinstance(ascending, bool):
      raise Exception("Sorry, ascending can only be boolean.")
    

    if comparison_type == 0:
      return dataframe[dataframe["num_words"] > limit_of_words].sort_values(ordered_by, ascending = ascending)
    else:
      return dataframe[dataframe["num_words"] <= limit_of_words].sort_values(ordered_by, ascending = ascending)
