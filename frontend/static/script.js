
async function fetchData(endpoint, place) {
    try {
        const response = await fetch(`${endpoint}${location.search}`);
        const responseData = await response.json();
        var displayDiv = document.getElementById(place);
        displayDiv.innerHTML = responseData;
        
    } catch (error) {
        console.error('Error fetching data:', error);
    }
};

const queryString = location.search;

fetchData('/neuralnetwork', 'nn');
fetchData('/naivebayes', 'nb');