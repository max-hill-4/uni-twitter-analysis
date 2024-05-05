
async function fetchData(endpoint) {
    try {
        // Make an AJAX request to the specified endpoint with the provided data
        const response = await fetch(`${endpoint}${location.search}`);
        const responseData = await response.json();

        // Work with the received data
        displayData(responseData);
    } catch (error) {
        console.error('Error fetching data:', error);
    }
};

function displayData(data) { 
    console.log(data)
};

const queryString = location.search;

fetchData('/twitterembed');
fetchData('/neuralnetwork');
fetchData('/naivebayes');


// Fetch tweet embed
// get string data from tweet
// pass string to following endpoints
// Fetch NN 
// send NB request
    