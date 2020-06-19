import requests
import re
import pandas as pd
from single_entry import SingleEntry
from bs4 import BeautifulSoup, SoupStrainer

class HackerNewsScraper:
  MAX_ENTRIES = 30

  def __init__(self):
    self.URL = 'https://news.ycombinator.com/'
    self.content = ""
    self.news = []

  def do_request(self):
    hacker_news_request = requests.get(self.URL)
    return hacker_news_request.content

  def get_columns_titles_and_ranks(self, objects):
    columns_class_title = objects.find_all('td', attrs={'class':'title'})
    columns_ranks = objects.find_all('td', attrs={'class':'title', 'align':'right'})
    columns_titles = [column for column in columns_class_title if column not in columns_ranks]
    return columns_ranks, columns_titles

  def get_columns_metrics_and_comments(self, objects):
     columns_metrics = objects.find_all('td', attrs={'class':'subtext'})
     return columns_metrics

  def get_content_of_columns(self, columns_ranks, columns_titles, columns_metrics):
    entries = []
    size = len(columns_ranks)
    for index in range(0,size):
      entry = SingleEntry()
      entry.rank = self.get_text(columns_ranks[index].find('span', attrs={'class':'rank'}))
      entry.title = self.get_text(columns_titles[index].find('a', attrs={'class':'storylink'}))
      entry.num_words = len(entry.title.split())
      entry.points =  self.sanitize_points(self.get_text(columns_metrics[index].find('span', attrs={'class':'score'})))
      entry.comments =  self.sanitize_comments(self.look_for_metrics(columns_metrics[index].select("a[href*=item]")))
      entries.append(entry)

    return entries

  def get_text(self,soup_object):
    if soup_object is None:
      return "NULL"
    else:
      return soup_object.text

  def sanitize_points(self,text):
    return self.convert_to_int("point",text.replace(" points",""))
  def sanitize_comments(self,text):
    return self.convert_to_int("comment",text.replace("\xa0comment","").replace("s",""))

  def look_for_metrics(self, metrics):
    if len(metrics) > 1:
      return self.get_text(metrics[1])
    else:
      return ""

  def convert_to_int(self, type_text, text):
    try:
      number = int(text)
    except Exception as err:
      number = -1
      print(str(type_text)+" "+str(text)+' does not contain anything convertible to int, the '+str(type_text)+' will be -1')

    return number

  def scrape(self):
    hacker_news_content = self.do_request()
    td_parser = SoupStrainer('td')
    td_objects = BeautifulSoup(hacker_news_content, 'html.parser', parse_only = td_parser)
    columns_ranks, columns_titles = self.get_columns_titles_and_ranks(td_objects)
    columns_metrics = self.get_columns_metrics_and_comments(td_objects)
    
    self.news = self.get_content_of_columns(columns_ranks,columns_titles, columns_metrics)
    if len(self.news) == self.MAX_ENTRIES:
      return 1
    else:
      return 0

    #print(self.news[["title","num_words"]])

  def to_dataframe(self):
    return pd.DataFrame([entry.__str__() for entry in self.news])

  def filter_news(self, comparison_type = 1, limit_of_words = 5 , ordered_by = "comments", ascending = False):
    dataframe =  self.to_dataframe()
    
    if comparison_type not in [0,1]:
      raise Exception("Sorry, you can only filter the limit of words: 1 = more than, 0 = less than or equal.")
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

