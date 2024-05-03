from model import Model

import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from nltk.corpus import twitter_samples
import numpy 

from statistics import mean 
class NeuralNetwork(Model):
    def _preprocess(self, tweets):
        
        #I would much prefer if both Models could inherit some data preprocessing.
        # TD : simplify this function. Can be done without method calls.

        tokenizer = Tokenizer(num_words=5000, oov_token='<OOV>')
        tokenizer.fit_on_texts(tweets)

        #Vectorizes every tweet
        sequences = tokenizer.texts_to_sequences(tweets)

        padded_sequences = pad_sequences(sequences, maxlen=100, truncating='post')

        return padded_sequences
        
    def trainmodel(self, pos_data, neg_data):

        padded_sequences = self._preprocess(pos_data + neg_data)
        labels = np.concatenate([np.ones(len(pos_data)), np.zeros(len(neg_data))])

        X_train, X_test, y_train, y_test = train_test_split(padded_sequences, labels, test_size=0.2, random_state=42)
        
        

        self.model = tf.keras.Sequential([
            tf.keras.layers.Embedding(5000, 16, input_length=100),
            tf.keras.layers.GlobalAveragePooling1D(),
            tf.keras.layers.Dense(24, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])

        # Compile the model
        self.model.compile (loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

        # Train the model
        self.model.fit(X_train, y_train, epochs=7, batch_size=16, validation_data=(X_test, y_test))

        # Evaluate the model
        #loss, accuracy = model.evaluate(X_test, y_test)
        #print("Test Accuracy:", accuracy)

    def classify(self, text):

        values = self.model.predict(text)
        avg = numpy.mean(values)
        return 'p' if avg > 0.5 else 'n'
if __name__ == "__main__": 

    from nltk.corpus import twitter_samples
    from nltk import download
    download('twitter_samples')

    # Load Twitter data
    positive_tweets = twitter_samples.strings('positive_tweets.json')
    negative_tweets = twitter_samples.strings('negative_tweets.json')

    model = NeuralNetwork()
    model.trainmodel(positive_tweets, negative_tweets)
    a = model._preprocess(positive_tweets[1501])
    print(model.classify(a))