document.addEventListener('DOMContentLoaded', async () => {
    const quotesContainer = document.getElementById('quotes-container');
    const refreshButton = document.getElementById('refresh-button');
    const searchInput = document.getElementById('search-input');
    const originalButtonText = refreshButton.textContent;

    let allQuotes = []; // To store all fetched quotes

    // Function to render quotes to the DOM
    function renderQuotes(quotesToRender) {
        // Clear previous quotes or messages
        quotesContainer.innerHTML = '';

        if (!quotesToRender || quotesToRender.length === 0) {
            quotesContainer.innerHTML = '<p>No quotes match your search or none available.</p>';
            return;
        }

        quotesToRender.forEach(quote => {
            const quoteDiv = document.createElement('div');
            quoteDiv.className = 'quote-item';

            const quoteText = document.createElement('blockquote');
            quoteText.className = 'quote-text';
            quoteText.textContent = `“${quote.text}”`;

            const quoteAuthor = document.createElement('p');
            quoteAuthor.className = 'quote-author';
            quoteAuthor.textContent = `— ${quote.author}`;

            quoteDiv.appendChild(quoteText);
            quoteDiv.appendChild(quoteAuthor);
            quotesContainer.appendChild(quoteDiv);
        });
    }

    // Function to fetch quotes from the API
    async function fetchQuotes() {
        if (refreshButton) {
            refreshButton.disabled = true;
            refreshButton.textContent = 'Loading...';
        }
        if (searchInput) {
            searchInput.value = ''; // Clear search input on refresh
        }
        // Display loading message while fetching
        quotesContainer.innerHTML = '<p>Loading quotes...</p>';

        try {
            const response = await fetch('/api/quotes');

            if (!response.ok) {
                let errorMsg = `Error fetching quotes: ${response.status} ${response.statusText}`;
                try {
                    const errorData = await response.json();
                    if (errorData && errorData.error) {
                        errorMsg = `Error fetching quotes: ${errorData.error}`;
                    }
                } catch (e) { /* Ignore if error data cannot be parsed */ }
                throw new Error(errorMsg);
            }

            const fetchedQuotes = await response.json();

            if (fetchedQuotes && fetchedQuotes.error) { // Handle API returning an error object
                 allQuotes = []; // Reset allQuotes
                 quotesContainer.innerHTML = `<p>Error: ${fetchedQuotes.error}</p>`;
            } else if (!fetchedQuotes || !Array.isArray(fetchedQuotes) || fetchedQuotes.length === 0) {
                allQuotes = []; // Reset allQuotes
                quotesContainer.innerHTML = '<p>No quotes found or an error occurred retrieving them.</p>';
            } else {
                allQuotes = fetchedQuotes; // Store fetched quotes
                renderQuotes(allQuotes); // Render all fetched quotes
            }

        } catch (error) {
            console.error('Fetch error:', error);
            allQuotes = []; // Reset allQuotes on error
            quotesContainer.innerHTML = `<p>Failed to load quotes. ${error.message}. Check console for more details.</p>`;
        } finally {
            if (refreshButton) {
                refreshButton.disabled = false;
                refreshButton.textContent = originalButtonText;
            }
        }
    }

    // Event listener for the refresh button
    if (refreshButton) {
        refreshButton.addEventListener('click', fetchQuotes);
    }

    // Event listener for the search input
    if (searchInput) {
        searchInput.addEventListener('input', () => {
            const searchTerm = searchInput.value.toLowerCase().trim();
            if (searchTerm === '') {
                renderQuotes(allQuotes); // If search is empty, show all quotes
            } else {
                const filteredQuotes = allQuotes.filter(quote =>
                    quote.text.toLowerCase().includes(searchTerm) ||
                    quote.author.toLowerCase().includes(searchTerm)
                );
                renderQuotes(filteredQuotes);
            }
        });
    }

    // Initial fetch of quotes when the page loads
    fetchQuotes();
});
