from .model import Model

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
        
        # Build vocap map.
        tokenizer = Tokenizer(num_words=5000, oov_token='<OOV>')
        tokenizer.fit_on_texts(self.pos_data + self.neg_data)

        #Vectorizes every tweet.
        sequences = tokenizer.texts_to_sequences(tweets)

        # Pads every tweet.
        padded_sequences = pad_sequences(sequences, maxlen=100, truncating='post')
        print(padded_sequences)
        return padded_sequences
        
    def _trainmodel(self):
        
        padded_sequences = self._preprocess(self.pos_data + self.neg_data)
        labels = np.concatenate([np.ones(len(self.pos_data)), np.zeros(len(self.neg_data))])

        X_train, X_test, y_train, y_test = train_test_split(padded_sequences, labels, test_size=0.2, random_state=42)
        
        

        model = tf.keras.Sequential([
            tf.keras.layers.Embedding(5000, 16, input_length=100),
            tf.keras.layers.GlobalAveragePooling1D(),
            tf.keras.layers.Dense(24, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])

        # Compile the model
        model.compile (loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

        # Train the model
        model.fit(X_train, y_train, epochs=7, batch_size=16, validation_data=(X_test, y_test))
        model.save(r'backend\ML\models\NeuralNetwork.keras')

    async def predict(self, text):

        text = self._preprocess(text)
        model = tf.keras.models.load_model(r'backend\ML\models\NeuralNetwork.keras')

        values = model.predict(text)
        print(values)
        avg = numpy.mean(values)
        print(avg)
        return 'p' if avg > 0.5 else 'n'

if __name__ == "__main__": 

    from nltk.corpus import twitter_samples
    from nltk import download
    download('twitter_samples')

    # Load Twitter data
    positive_tweets = twitter_samples.strings('positive_tweets.json')
    negative_tweets = twitter_samples.strings('negative_tweets.json')
    print(positive_tweets[3])
    model = NeuralNetwork(positive_tweets, negative_tweets)
    #model._trainmodel()
    print(model.predict(positive_tweets[3]))
