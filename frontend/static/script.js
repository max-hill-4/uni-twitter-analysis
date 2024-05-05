
function fetchTwitterEmbed(tweetURL) {
    // URL of Twitter's oEmbed API
    var oEmbedURL = 'https://publish.twitter.com/oembed?url=' + encodeURIComponent(tweetURL);

    // Fetch the embed data from Twitter's oEmbed API
    fetch(oEmbedURL)
        .then(response => response.json())
        .then(data => {
            // Insert the HTML provided by Twitter into the specified element
            document.getElementById('twitter-widget').innerHTML = data.html;
        })
        .catch(error => console.error('Error fetching Twitter embed:', error));
}





async function fetchML(endpoint, data) {
    try {
        // Make an AJAX request to the specified endpoint with the provided data
        const response = await fetch(`${endpoint}?data=${encodeURIComponent(data)}`);
        const responseData = await response.json();

        // Work with the received data
        displayData(responseData);
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

function displayData(data) { 
    console.log(data)
}

fetchTwitterEmbed(data)
var data2 = "hello please test me im happy!"
fetchML('/neuralnetwork', data2);
fetchML('/naivebayes', data2);


// Fetch tweet embed
// get string data from tweet
// pass string to following endpoints
// Fetch NN 
// send NB request
    