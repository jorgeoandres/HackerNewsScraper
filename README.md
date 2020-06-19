# HackerNewsScraper
Simple Hacker News Scraper for the first 30 entries of the page. Filtering method is available.
It uses the web page: https://news.ycombinator.com to scrap information about the first 30 entries. The code just scrap the following attributes of each entry:
<ul>
<li>Rank</li>
<li>Title</li>
<li>Points</li>
<li>Comments</li>
</ul>

## Requirements
Some libraries are required to use the Scraper:
<ul>
<li>pandas</li>
<li>beautifulsoup4</li>
<li>pytest</li>
<li>request</li>
</ul>

You can install them individually by using pip or use pip install command with the provided `require` file.
```python
pip install -r require
```
## Main file
It provides a main file to demostrate the use of HackerNewsScraper. First, it shows the entries. Second, shows the filtered dataframe of entries with more than five words in the title ordered by the amount of comments first. Finally, it uses the filtering method to show entries with less than or equal to five words in the title ordered by points.

```python
python main.py
```
## Tests
By using PyTest we provide four test cases. You can test them with 
```python
py.test -q test_scraper.py
```
