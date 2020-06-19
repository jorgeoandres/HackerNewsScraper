from hacker_news_scraper import HackerNewsScraper

if __name__ == "__main__":
    scraper = HackerNewsScraper()
    success = scraper.scrape()
    
    print("All entries")
    print(scraper.to_dataframe())
    print("*************************\n")

    print("Entries with title with more than or equal to "+str(5)+" words ordered by comments:")
    print(scraper.filter_news(0,5,"comments"))
    print("*************************\n")

    print("Entries with title with less than or equal to "+str(5)+" words ordered by points:")
    print(scraper.filter_news(1,5,"points"))
    print("*************************\n")