"""
This script is responsible for scraping quotes from the website http://quotes.toscrape.com/.
It provides a function to fetch and parse the quotes, returning them as a list of dictionaries.
"""
import requests
from bs4 import BeautifulSoup

def scrape_quotes():
    """
    Fetches quotes from http://quotes.toscrape.com/.

    The function sends a GET request to the specified URL, parses the HTML content,
    and extracts quote texts and their corresponding authors.

    Returns:
        list: A list of dictionaries, where each dictionary has the keys 'text' and 'author'.
              Returns an empty list if an error occurs during fetching or parsing,
              or if no quotes are found.
    """
    quotes_list = []
    url = "http://quotes.toscrape.com/"

    try:
        response = requests.get(url, timeout=10) # Added timeout
        response.raise_for_status()  # Raises an HTTPError for bad responses (4XX or 5XX)

        soup = BeautifulSoup(response.content, 'html.parser')
        quote_elements = soup.find_all('div', class_='quote')

        for quote_element in quote_elements:
            text_element = quote_element.find('span', class_='text')
            author_element = quote_element.find('small', class_='author')

            if text_element and author_element:
                quote_text = text_element.get_text(strip=True)
                author_name = author_element.get_text(strip=True)
                quotes_list.append({'text': quote_text, 'author': author_name})
            else:
                print("Warning: Could not extract text or author from a quote element.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return [] # Return empty list on error
    except Exception as e: # Catch any other unexpected errors during parsing
        print(f"An error occurred during parsing: {e}")
        return []


    return quotes_list

if __name__ == '__main__':
    scraped_quotes = scrape_quotes()
    if scraped_quotes:
        print("Scraped Quotes:")
        for i, quote_data in enumerate(scraped_quotes):
            print(f"\nQuote {i+1}:")
            print(f"  Text: {quote_data['text']}")
            print(f"  Author: {quote_data['author']}")
    else:
        print("No quotes were scraped or an error occurred.")
