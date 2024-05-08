import unittest
from unittest.mock import patch
import joblib
from NaiveBayes import NaiveBayes
from NeuralNetwork import NeuralNetwork

class TestNaiveBayes(unittest.TestCase):
    

    @patch.object(NaiveBayes, "_preprocess")
    def test__stopword__removal(self, mock_method):

        tweet = "this is a tweet with stopwords"
        _STOPWORDS = ["a", "the", "is", "with"]
        data = NaiveBayes()._preprocess(tweet)
        expected_data = expected_data = ['this', 'tweet', 'stopwords']
        self.assertEqual(data, expected_data)

class TestNeuralNetwork(unittest.TestCase):
    def setUp(self):
        # Initialize your NeuralNetwork instance with appropriate data
        self.neural_network = NeuralNetwork()

    def test_preprocess_sequence_length(self):
        # Mock input data
        tweets = ["This is a test tweet."]

        # Call the _preprocess method
        processed_sequences = self.neural_network._preprocess(tweets)

        # Check if the length of the processed sequence is 100
        self.assertEqual(len(processed_sequences[0]), 100, "Length of processed sequence is not 100")

if __name__ == "__main__":
    unittest.main()