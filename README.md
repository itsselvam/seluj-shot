# Quote Scraper and Display App

## Description
This application scrapes quotes from [quotes.toscrape.com](http://quotes.toscrape.com/), provides them via a JSON API, and displays them on a simple web interface.

## Features
- Scrapes quotes and authors.
- JSON API endpoint (`/api/quotes`).
- Web interface to view quotes.
- Basic responsive design.
- Unit tests for backend.
- Refresh Button: Allows manually re-fetching and updating the displayed quotes.
- Client-Side Search: Filter quotes in real-time by typing keywords for quote text or author.
- Displays an image (currently a placeholder) above each quote.

## Setup and Installation

1.  **Clone repository:** `git clone <url>` & `cd <dir>`
2.  **Create & activate venv:**
    *   macOS/Linux: `python3 -m venv venv && source venv/bin/activate`
    *   Windows: `python -m venv venv && venv\Scripts\activate`
3.  **Install dependencies:** `pip install -r requirements.txt`

## Running the Application

1.  **Run Backend (Flask):**
    From project root:
    ```bash
    # Recommended:
    export FLASK_APP=backend.app # macOS/Linux
    # set FLASK_APP=backend.app # Windows cmd.exe
    # $env:FLASK_APP="backend.app" # Windows PowerShell
    flask run
    ```
    Alternatively: `python backend/app.py`
    Server runs at `http://localhost:5000`.

2.  **View Frontend:**
    Open `frontend/index.html` in a browser (backend must be running).
    Once loaded, you can use the "Refresh Quotes" button to fetch a new set of quotes, or use the search bar to filter the currently displayed quotes by text or author.

## Running Tests
From project root:
```bash
python -m unittest discover -s tests -p 'test_*.py'
```

## Image Generation Configuration

This application is structured to display an image alongside each quote. Currently, it uses placeholder images from `picsum.photos`.

To enable actual image generation using Google's Gemini API (or any other image generation service):

1.  You need to implement the image generation logic within the `get_image_url_for_quote(quote_text)` function located in `backend/scraper.py`.
    *   The relevant section in `backend/scraper.py` is marked with a `DEVELOPER NOTE`.
2.  This function should be modified to call the desired image generation API, using your own API key and any necessary authentication.
3.  **Important**: Securely manage your API keys. Do not hardcode them directly into the script. Use environment variables or a secure configuration management system.
4.  The function must return a valid image URL string for the frontend to display.
5.  Ensure any new libraries required for your chosen image generation API are added to `requirements.txt`.

## Project Structure
-   **`backend/`**: Flask app (`app.py`) & scraper (`scraper.py`).
-   **`frontend/`**: UI (`index.html`, `styles.css`, `script.js`).
-   **`tests/`**: Backend unit tests (`test_backend.py`).
-   **`requirements.txt`**: Python dependencies.
-   **`.gitignore`**: Git ignore rules.
-   **`README.md`**: This file.