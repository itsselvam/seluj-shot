"""
This script implements a Flask web application that serves scraped quotes via an API endpoint.
It uses the scraper module to fetch quotes and provides them in JSON format.
"""
from flask import Flask, jsonify
from .scraper import scrape_quotes # Relative import

app = Flask(__name__)

@app.route('/api/quotes', methods=['GET'])
def get_quotes():
    """
    Handles GET requests to the /api/quotes endpoint.

    This function calls the `scrape_quotes` function to obtain a list of quotes.
    It then returns these quotes as a JSON response. If scraping fails or no
    quotes are available, it returns an appropriate JSON error message with a
    500 status code.

    Returns:
        flask.Response: A JSON response containing a list of quotes (on success)
                        or an error message (on failure).
    """
    try:
        quotes_list = scrape_quotes()
        if quotes_list: # Checks if the list is not empty
            return jsonify(quotes_list)
        else:
            # This case handles when scrape_quotes returns an empty list (e.g., due to scraping issues or no quotes found)
            # or if scrape_quotes itself had an error and returned an empty list as per its own error handling.
            return jsonify({'error': 'Could not retrieve quotes or no quotes available'}), 500
    except Exception as e:
        # This is a fallback for unexpected errors in this function itself or if scrape_quotes raises an unhandled exception.
        # Log the exception for debugging purposes
        app.logger.error(f"An unexpected error occurred in get_quotes: {e}")
        return jsonify({'error': 'An unexpected server error occurred'}), 500

if __name__ == '__main__':
    # Running on 0.0.0.0 makes the server accessible externally, e.g., from the host machine if port mapping is set up.
    # Port 5000 is a common default for Flask apps.
    app.run(debug=True, host='0.0.0.0', port=5000)
