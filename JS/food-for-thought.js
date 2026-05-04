(() => {
  const quoteText = document.querySelector('[data-quote-text]');
  const quoteMeta = document.querySelector('[data-quote-meta]');
  const refreshButton = document.querySelector('[data-quote-refresh]');

  if (!quoteText || !quoteMeta) {
    return;
  }

  const scriptSrc = document.currentScript && document.currentScript.src
    ? document.currentScript.src
    : window.location.href;
  const quotesUrl = new URL('../data/food-for-thought.json', scriptSrc);

  let quotes = [];

  const renderRandomQuote = () => {
    if (!Array.isArray(quotes) || quotes.length === 0) {
      quoteText.textContent = 'Unable to load a philosophy quote right now.';
      quoteMeta.textContent = '';
      return;
    }

    const quote = quotes[Math.floor(Math.random() * quotes.length)];
    const parts = [quote.author, quote.work, quote.section].filter(Boolean);

    quoteText.textContent = quote.quote;
    quoteMeta.textContent = parts.join(' — ');
  };

  fetch(quotesUrl)
    .then((response) => {
      if (!response.ok) {
        throw new Error(`Failed to load quotes: ${response.status} ${response.statusText}`);
      }
      return response.json();
    })
    .then((data) => {
      if (!Array.isArray(data) || data.length === 0) {
        throw new Error('Quote data is empty or malformed.');
      }

      quotes = data;
      renderRandomQuote();

      if (refreshButton) {
        refreshButton.addEventListener('click', renderRandomQuote);
      }
    })
    .catch((error) => {
      console.error('Food for Thought could not be loaded:', error);
      quoteText.textContent = 'Unable to load a philosophy quote right now.';
      quoteMeta.textContent = '';

      if (refreshButton) {
        refreshButton.disabled = true;
      }
    });
})();
