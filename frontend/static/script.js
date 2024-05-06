
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
    if (status === 'p') {
        statusBox.style.backgroundColor = 'green';
    } else {
        statusBox.style.backgroundColor = 'red';
    }
  }
const queryString = document.getElementById('tweet').textContent;

fetchML('/neuralnetwork', 'nn');
fetchML('/naivebayes', 'nb');