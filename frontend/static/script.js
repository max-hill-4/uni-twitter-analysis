
async function fetchML(endpoint, place) {
    try {
        const response = await fetch(`${endpoint}?query=${queryString}`);
        const responseData = await response.json();
        updateStatus(responseData, place)
        
    } catch (error) {
        console.error('Error fetching data:', error);
    }
};

function updateStatus(status, place) {
    const statusBox = document.getElementById(place);
    const sentimentText = status === 'p' ? 'Positive' : 'Negative';
    const sentimentSpan = document.getElementById(place + '-sentiment');
    sentimentSpan.textContent = sentimentText;

    if (status === 'p') {
        statusBox.style.backgroundColor = "#42f545";
    } else {
        statusBox.style.backgroundColor = "#f54242";
    }
}

const queryString = document.getElementById('tweet').textContent;

fetchML('/neuralnetwork', 'nn');
fetchML('/naivebayes', 'nb');