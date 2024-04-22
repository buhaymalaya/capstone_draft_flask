const apiKey211 = ')i;MR%%3Lt_k,Ku'; // Waiting for request to be granted, api key still invalid
const apiUrl = 'https://api.211.org';

const searchBtn = document.getElementById('search-btn');
const searchTermInput = document.getElementById('search-term');
const locationInput = document.getElementById('location');
const searchResultsContainer = document.getElementById('search-results');

searchBtn.addEventListener('click', () => {
    const searchTerm = searchTermInput.value.trim();
    const location = locationInput.value.trim();

    if (!searchTerm) {
        alert('Please enter a search term such as service needed, location, etc.');
        return;
    }

    searchAPI(searchTerm, location);
});

const searchAPI = async (searchTerm, location) => {
    try {
        const response = await fetch(`${apiUrl}/search/v1/api/Search/Keyword?Keyword=${searchTerm}&Top=10&OrderBy=Relevance&SearchMode=Any&IncludeStateNationalRecords=true&ReturnTaxonomyTermsIfNoResults=false&SearchWithin=false`, {
            headers: {
                'Api-Key': apiKey211
            }
        });
        const data = await response.json();
        displaySearchResults(data);
    } catch (error) {
        console.error('Error searching:', error);
        alert('An error occurred while searching. Please try again.');
    }
}

const displaySearchResults = (data) => {
    searchResultsContainer.innerHTML = ''; // Clear previous results

    if (data && data.results && data.results.length > 0) {
        data.results.forEach(result => {
            const resultDiv = document.createElement('div');
            resultDiv.innerHTML = `
                <p><strong>Title:</strong> ${result.title}</p>
                <p><strong>Description:</strong> ${result.description}</p>
                <p><strong>Location:</strong> ${result.location}</p>
            `;
            searchResultsContainer.appendChild(resultDiv);
        });
    } else {
        searchResultsContainer.innerHTML = '<p>No results found.</p>';
    }
}
