from model import Model

import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from nltk.corpus import twitter_samples

class NeuralNetwork(Model):
    def _preprocess(self):
        
        # TD : simplify this function. Can be done without method calls.
        labels = np.concatenate([np.ones(len(self.pos_data)), np.zeros(len(self.neg_data))])

        tokenizer = Tokenizer(num_words=5000, oov_token='<OOV>')

        tweets = self.pos_data + self.neg_data
        tokenizer.fit_on_texts(tweets)

        #Vectorizes every tweet
        sequences = tokenizer.texts_to_sequences(tweets)

        # Makes every item of length 100 using 0 as padding
        padded_sequences = pad_sequences(sequences, maxlen=100, truncating='post')

        # Split the data into training and testing sets
        return train_test_split(padded_sequences, labels, test_size=0.2, random_state=42)
    
    def trainmodel(self):

        X_train, X_test, y_train, y_test = self._preprocess()

        self.model = tf.keras.Sequential([
            tf.keras.layers.Embedding(5000, 16, input_length=100),
            tf.keras.layers.GlobalAveragePooling1D(),
            tf.keras.layers.Dense(24, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])

        # Compile the model
        self.model.compile (loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

        # Train the model
        self.model.fit(X_train, y_train, epochs=5, batch_size=16, validation_data=(X_test, y_test))

        # Evaluate the model
        #loss, accuracy = model.evaluate(X_test, y_test)
        #print("Test Accuracy:", accuracy)

    def classify(self, text):
        print(self.model.predict(text))

if __name__ == "__main__": 
    from nltk.corpus import twitter_samples
    from nltk import download
    download('twitter_samples')

    # Load Twitter data
    positive_tweets = twitter_samples.strings('positive_tweets.json')
    negative_tweets = twitter_samples.strings('negative_tweets.json')

    model = NeuralNetwork(positive_tweets, negative_tweets)
    model.trainmodel()
    # it hink i would also need to convert this into a frickin VECTOR MAN OKAY TOMMOROW JOB MAN GJ TODAY.
    model.classify("good good good good")