document.addEventListener('DOMContentLoaded', async () => {
    const quotesContainer = document.getElementById('quotes-container');

    async function fetchQuotes() {
        try {
            // Assuming the backend API is available at '/api/quotes' on the same host.
            // If running frontend separately from backend (e.g. live server vs python flask server)
            // you might need the full URL: 'http://localhost:5000/api/quotes'
            const response = await fetch('/api/quotes');

            if (!response.ok) {
                // Try to get error message from response body if available
                let errorMsg = `Error fetching quotes: ${response.status} ${response.statusText}`;
                try {
                    const errorData = await response.json();
                    if (errorData && errorData.error) {
                        errorMsg = `Error fetching quotes: ${errorData.error}`;
                    }
                } catch (e) {
                    // Could not parse error JSON, stick with status text
                }
                throw new Error(errorMsg);
            }

            const quotes = await response.json();

            if (!quotes || quotes.length === 0) {
                quotesContainer.innerHTML = '<p>No quotes found or an error occurred retrieving them.</p>';
                // Check if the response was actually an error object like {'error': 'message'}
                // This case can happen if API returns 200 OK but an empty list or an error structure.
                if (quotes && quotes.error) {
                     quotesContainer.innerHTML = `<p>Error: ${quotes.error}</p>`;
                }
                return;
            }

            // Clear "Loading quotes..." message
            quotesContainer.innerHTML = '';

            quotes.forEach(quote => {
                const quoteDiv = document.createElement('div');
                quoteDiv.className = 'quote-item';

                const quoteText = document.createElement('blockquote');
                quoteText.className = 'quote-text';
                quoteText.textContent = `“${quote.text}”`; // Add quotation marks

                const quoteAuthor = document.createElement('p');
                quoteAuthor.className = 'quote-author';
                quoteAuthor.textContent = `— ${quote.author}`;

                quoteDiv.appendChild(quoteText);
                quoteDiv.appendChild(quoteAuthor);
                quotesContainer.appendChild(quoteDiv);
            });

        } catch (error) {
            console.error('Fetch error:', error);
            quotesContainer.innerHTML = `<p>Failed to load quotes. ${error.message}. Check console for more details.</p>`;
        }
    }

    fetchQuotes();
});
