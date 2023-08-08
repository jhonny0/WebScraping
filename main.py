import csv
import requests
from bs4 import BeautifulSoup
from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd
import nltk
nltk.download('vader_lexicon')

class QuoteScraper:
    def __init__(self, url):
        self.url = url

    def scrape(self):
        quotes = []
        while True:
            response = requests.get(self.url)
            soup = BeautifulSoup(response.text, "html.parser")

            quote_divs = soup.find_all("div", class_="quote")
            for quote_div in quote_divs:
                text = quote_div.find("span", class_="text").get_text()
                author = quote_div.find("small", class_="author").get_text()
                quotes.append((text, author))

            next_page = soup.find("li", class_="next")
            if next_page is None:
                break
            self.url = "http://quotes.toscrape.com" + next_page.find("a")["href"]

        return quotes


class CSVWriter:
    def __init__(self, filename):
        self.filename = filename

    def write(self, quotes):
        with open(self.filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Quote", "Author"])
            for quote in quotes:
                writer.writerow(quote)


class SentimentAnalyzer:
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()

    def analyze(self, filename):
        df = pd.read_csv(filename)
        df['Sentiment'] = df['Quote'].apply(lambda quote: self.sia.polarity_scores(quote))
        print(df.head())


# Use the classes
scraper = QuoteScraper("http://quotes.toscrape.com")
quotes = scraper.scrape()

writer = CSVWriter('quotes.csv')
writer.write(quotes)

analyzer = SentimentAnalyzer()
analyzer.analyze('quotes.csv')
