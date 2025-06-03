"""
This script is responsible for scraping quotes from the website http://quotes.toscrape.com/.
It provides a function to fetch and parse the quotes, returning them as a list of dictionaries.
Each dictionary includes the quote text, author, and a placeholder image URL.
"""
import requests
from bs4 import BeautifulSoup
import re # For sanitizing seed for picsum.photos

# DEVELOPER NOTE: This is a placeholder function.
# To enable actual image generation via Gemini:
# 1. Implement the Gemini API call here.
# 2. Use the provided API key securely (e.g., via environment variables).
# 3. Ensure the function returns a valid image URL string.
# 4. Handle potential errors from the API call.
def get_image_url_for_quote(quote_text):
    """
    Generates a placeholder image URL for a given quote text using picsum.photos.
    The seed for the image is derived from the quote text.

    Args:
        quote_text (str): The text of the quote.

    Returns:
        str: A URL string for a placeholder image.
    """
    if not quote_text:
        seed = "default-quote"
    else:
        # Sanitize and shorten the quote text to create a seed
        # Remove non-alphanumeric characters (except hyphens) and replace spaces with hyphens
        seed = re.sub(r'[^\w\s-]', '', quote_text.lower())
        seed = re.sub(r'\s+', '-', seed)[:50] # Limit length of seed
        if not seed: # if seed becomes empty after sanitization
            seed = "random-quote-" + str(len(quote_text))


    return f"https://picsum.photos/seed/{seed}/400/300" # Standardized image size

def scrape_quotes():
    """
    Fetches quotes from http://quotes.toscrape.com/.

    The function sends a GET request to the specified URL, parses the HTML content,
    and extracts quote texts and their corresponding authors. It also generates
    a placeholder image URL for each quote.

    Returns:
        list: A list of dictionaries, where each dictionary has the keys 'text',
              'author', and 'image_url'. Returns an empty list if an error occurs
              during fetching or parsing, or if no quotes are found.
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

                image_url = get_image_url_for_quote(quote_text)

                quotes_list.append({
                    'text': quote_text,
                    'author': author_name,
                    'image_url': image_url
                })
            else:
                print("Warning: Could not extract text, author from a quote element.")

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
            print(f"  Image URL: {quote_data['image_url']}")
    else:
        print("No quotes were scraped or an error occurred.")
