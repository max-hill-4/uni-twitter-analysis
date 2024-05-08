import unittest
from unittest.mock import patch
import joblib
from NaiveBayes import NaiveBayes


class TestNaiveBayes(unittest.TestCase):
    

    @patch.object(NaiveBayes, "_preprocess")
    def test__stopword__removal(self, mock_method):

        tweet = "this is a tweet with stopwords"
        _STOPWORDS = ["a", "the", "is", "with"]
        data = mock_method(tweet)
        expected_data = []
        for word in tweet.split():
            if word not in _STOPWORDS:
                expected_data.append(word)
        self.assertEqual()


if __name__ == "__main__":
    unittest.main()